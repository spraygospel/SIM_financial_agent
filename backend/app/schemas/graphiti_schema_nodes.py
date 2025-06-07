# File: backend/app/schemas/graphiti_schema_nodes.py

from pydantic import BaseModel, Field
from typing import Optional, List
import uuid

# Namespace UUID untuk menghasilkan UUID deterministik untuk skema
# Anda bisa mengganti UUID ini dengan UUID acak lain yang Anda generate sekali dan simpan
NAMESPACE_AI_AGENT_SCHEMA = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8") # Contoh Namespace DNS

class GraphitiBaseNode(BaseModel):
    uuid: str = Field(description="UUID unik untuk node ini.")
    group_id: str = Field(description="Group ID untuk namespacing dalam Graphiti.")
    # Graphiti secara otomatis akan menambahkan label berdasarkan nama kelas saat menyimpan
    # Kita bisa menambahkan field 'labels' jika ingin lebih eksplisit, tapi biasanya tidak perlu jika struktur kelas jelas

class DatabaseColumnNode(GraphitiBaseNode):
    column_name: str = Field(..., description="Nama kolom database.")
    description: Optional[str] = Field(default=None, description="Deskripsi fungsional kolom.")
    classification: Optional[str] = Field(default=None, description="Klasifikasi semantik kolom.")
    is_aggregatable: Optional[bool] = Field(default=None, description="Apakah kolom ini bisa diagregasi.")
    type_from_db: Optional[str] = Field(default=None, description="Tipe data asli dari database MySQL.")
    # Atribut tambahan yang mungkin berguna dari hasil riset Graphiti, jika kita ingin menambahkannya nanti:
    # data_type: Optional[str] = Field(default=None, description="Tipe data kolom, e.g., VARCHAR, INTEGER.") # Redundan dengan type_from_db untuk saat ini
    # is_primary_key: bool = Field(default=False)
    # is_foreign_key: bool = Field(default=False)
    # references_table_name: Optional[str] = Field(default=None) # Untuk foreign key, nama tabel tujuan
    # references_column_name: Optional[str] = Field(default=None) # Untuk foreign key, nama kolom tujuan

    @classmethod
    def create_uuid(cls, group_id: str, table_name: str, column_name: str) -> str:
        return str(uuid.uuid5(NAMESPACE_AI_AGENT_SCHEMA, f"{group_id}.{table_name}.{column_name}"))

class DatabaseTableNode(GraphitiBaseNode):
    table_name: str = Field(..., description="Nama tabel database.")
    purpose: Optional[str] = Field(default=None, description="Deskripsi tujuan tabel.")
    business_category: Optional[str] = Field(default=None, description="Kategori bisnis tabel.")
    # columns: List[DatabaseColumnNode] = Field(default_factory=list, description="Daftar kolom dalam tabel ini.")
    # Kita akan membuat relasi HAS_COLUMN secara eksplisit, jadi 'columns' di sini mungkin tidak perlu disimpan sebagai atribut langsung di TableNode Graphiti
    # kecuali jika Graphiti secara otomatis membuat struktur nested. Untuk saat ini, kita fokus pada node dan relasi terpisah.

    @classmethod
    def create_uuid(cls, group_id: str, table_name: str) -> str:
        return str(uuid.uuid5(NAMESPACE_AI_AGENT_SCHEMA, f"{group_id}.{table_name}"))

class GraphitiBaseEdge(BaseModel):
    uuid: str = Field(description="UUID unik untuk edge ini.")
    group_id: str = Field(description="Group ID untuk namespacing dalam Graphiti.")
    source_node_uuid: str = Field(description="UUID dari node sumber.")
    target_node_uuid: str = Field(description="UUID dari node target.")
    name: str = Field(description="Nama atau tipe dari edge/relasi.") # Misal: HAS_COLUMN, REFERENCES

    @classmethod
    def create_uuid(cls, group_id: str, source_uuid: str, target_uuid: str, edge_name: str) -> str:
        return str(uuid.uuid5(NAMESPACE_AI_AGENT_SCHEMA, f"{group_id}.{source_uuid}.{target_uuid}.{edge_name}"))

class HasColumnEdge(GraphitiBaseEdge):
    name: str = Field(default="HAS_COLUMN", description="Tipe relasi: Table HAS_COLUMN Column.")
    # Atribut tambahan spesifik untuk edge HAS_COLUMN jika ada

class ReferencesEdge(GraphitiBaseEdge):
    name: str = Field(default="REFERENCES", description="Tipe relasi: Column REFERENCES Column.")
    # Atribut tambahan seperti 'constraint_name' atau 'relationship_type' (one-to-many, etc.)
    # bisa ditambahkan di sini jika diperlukan dan didukung Graphiti untuk disimpan di edge.
    # Untuk MVP, tipe 'REFERENCES' mungkin cukup.