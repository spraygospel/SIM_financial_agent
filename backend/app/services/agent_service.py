# backend/app/services/agent_service.py
from typing import Dict, Any, Union, Optional, List
import uuid
import sys
from datetime import datetime

from backend.app.langgraph_workflow.graph import app_graph
from backend.app.schemas.agent_state import AgentState, TimePeriod, MCPToolCallLog # Impor semua yang dibutuhkan
from backend.app.schemas.api_models import (
    QueryRequest, 
    QueryResponseSuccess, 
    QueryResponseError, 
    DataSourceDetails, 
    ExecutiveSummaryItem 
)
from backend.app.core.config import settings


class AgentService:
    async def process_query(
        self, 
        session_id: str, 
        user_query: str,
    ) -> Union[QueryResponseSuccess, QueryResponseError]:
        
        print(f"AgentService: process_query called for session_id: {session_id}", file=sys.stderr)

        initial_state: AgentState = {
            "user_query": user_query,
            "session_id": session_id,
            "conversation_history": [], 
            "mcp_tool_call_history": [],
            "workflow_status": "processing",
        }

        config = {"configurable": {"session_id": session_id}}

        try:
            final_state_dict: Optional[AgentState] = None
            
            async for event_part in app_graph.astream(initial_state, config=config):
                current_node_states = {k: v for k, v in event_part.items() if k != "__end__"}
                if current_node_states:
                    for node_name, node_state in current_node_states.items():
                        if isinstance(node_state, dict): # Pastikan itu state dictionary
                            final_state_dict = node_state
                        break
                
                if "__end__" in event_part:
                    break 
            
            if not final_state_dict:
                print("AgentService: final_state_dict is None after streaming graph (no state captured before __end__).", file=sys.stderr)
                return QueryResponseError(
                    session_id=session_id,
                    error_type="WORKFLOW_ERROR",
                    user_message="Terjadi kesalahan internal saat memproses permintaan Anda (workflow tidak menghasilkan state akhir yang valid).",
                    technical_details="final_state_dict was None after graph execution stream. Could not capture state from the last node."
                )

            print(f"AgentService: Final state from LangGraph for session {session_id}: {final_state_dict.get('workflow_status')}", file=sys.stderr)

            if final_state_dict.get("workflow_status") == "completed":
                
                ds_info_from_state: Optional[Dict[str, Any]] = final_state_dict.get("data_source_info")
                data_source_details_obj: Optional[DataSourceDetails] = None # Ubah nama variabel
                if isinstance(ds_info_from_state, dict):
                    data_source_details_obj = DataSourceDetails(
                        description=ds_info_from_state.get("description"),
                        tables_used=ds_info_from_state.get("tables_used", []),
                        join_details=ds_info_from_state.get("join_details", []),
                        filters_applied=ds_info_from_state.get("filters_applied", []),
                        report_generated_at=datetime.utcnow().strftime("%d %b %Y, %H:%M:%S WIB")
                    )
                
                summary_from_state: Optional[List[Dict[str,str]]] = final_state_dict.get("executive_summary")
                exec_summary_items: List[ExecutiveSummaryItem] = []
                if summary_from_state:
                    for item_dict in summary_from_state:
                        if isinstance(item_dict, dict) and "metric_name" in item_dict and "value" in item_dict and "label" in item_dict:
                             exec_summary_items.append(ExecutiveSummaryItem(**item_dict))
                        else:
                            print(f"AgentService: Invalid item in executive_summary: {item_dict}", file=sys.stderr)
                
                return QueryResponseSuccess(
                    session_id=session_id,
                    final_narrative=final_state_dict.get("final_narrative", "Tidak ada narasi."),
                    data_table_for_display=final_state_dict.get("data_table_for_display", []),
                    executive_summary=exec_summary_items,
                    warnings_for_display=final_state_dict.get("warnings_for_display", []),
                    data_source_info=data_source_details_obj, # Gunakan objek yang sudah dibuat
                    data_quality_score=final_state_dict.get("quality_score")
                )
            else: 
                user_msg = final_state_dict.get("error_message_for_user", "Terjadi kesalahan yang tidak diketahui.")
                tech_details = final_state_dict.get("technical_error_details", "Tidak ada detail teknis.")
                # Error type bisa diambil dari state jika node error mengisinya
                error_type_from_state = final_state_dict.get("current_node_name", "AGENT") + "_ERROR" if final_state_dict.get("error_message_for_user") else "AGENT_PROCESSING_ERROR"

                print(f"AgentService: Workflow error for session {session_id}. User msg: {user_msg}. Tech details: {tech_details}", file=sys.stderr)
                return QueryResponseError(
                    session_id=session_id,
                    error_type=error_type_from_state,
                    user_message=user_msg,
                    technical_details=tech_details 
                )

        except Exception as e:
            print(f"AgentService: Unhandled exception during agent processing for session {session_id}: {str(e)}", file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)
            return QueryResponseError(
                session_id=session_id,
                error_type="UNHANDLED_EXCEPTION_IN_SERVICE",
                user_message="Terjadi kesalahan internal server yang tidak terduga saat memproses permintaan.",
                technical_details=str(e)
            )

agent_service_instance = AgentService()