# backend/app/api/v1/endpoints/query.py
from fastapi import APIRouter, HTTPException, Body
from typing import Union, Optional, List, Dict, Any
import sys 

from backend.app.schemas.api_models import (
    QueryRequest, 
    QueryResponseSuccess, 
    QueryResponseError,
    DataSourceDetails,      # Pastikan ini diimpor
    ExecutiveSummaryItem    # Pastikan ini diimpor
)
from backend.app.services.agent_service import agent_service_instance 

router = APIRouter()

@router.post(
    "", 
    response_model=Union[QueryResponseSuccess, QueryResponseError],
    summary="Process a natural language query for the AI Agent",
    response_description="Returns the agent's analysis, data, or an error message."
)
async def process_query_endpoint(request_data: QueryRequest = Body(...)) -> Union[QueryResponseSuccess, QueryResponseError]:
    print(f"--- API Endpoint /api/v1/query POST request received ---", file=sys.stderr) 
    print(f"Session ID: {request_data.session_id}, User Query: '{request_data.user_query}'", file=sys.stderr)

    if not request_data.user_query.strip():
        print(f"API Endpoint: User query is empty for session_id: {request_data.session_id}", file=sys.stderr)
        return QueryResponseError(
            session_id=request_data.session_id,
            error_type="REQUEST_VALIDATION_ERROR",
            user_message="Pertanyaan tidak boleh kosong.",
            technical_details="User query was empty or contained only whitespace."
        )

    try:
        # AgentService akan mengembalikan instance dari QueryResponseSuccess atau QueryResponseError
        response_from_service = await agent_service_instance.process_query(
            session_id=request_data.session_id,
            user_query=request_data.user_query
        )
        
        # Tidak perlu lagi unpack dan rebuild di sini karena service sudah mengembalikan model Pydantic yang benar.
        # Cukup kembalikan hasil dari service.
        if isinstance(response_from_service, QueryResponseSuccess):
            print(f"API Endpoint: Successfully processed query for session {request_data.session_id}. Returning QueryResponseSuccess.", file=sys.stderr)
        elif isinstance(response_from_service, QueryResponseError):
            print(f"API Endpoint: Error processing query for session {request_data.session_id}. Returning QueryResponseError. Type: {response_from_service.error_type}", file=sys.stderr)
        
        return response_from_service

    except Exception as e:
        # Exception ini seharusnya ditangkap di AgentService, tapi sebagai fallback terakhir.
        error_msg = f"Tidak terduga: Kesalahan internal server saat memanggil agent service: {str(e)}"
        print(error_msg, file=sys.stderr) 
        import traceback
        traceback.print_exc(file=sys.stderr)
        return QueryResponseError(
            session_id=request_data.session_id,
            error_type="UNHANDLED_API_EXCEPTION",
            user_message="Terjadi kesalahan internal pada server API. Silakan coba lagi nanti.",
            technical_details=f"Unhandled exception in API endpoint: {str(e)}"
        )