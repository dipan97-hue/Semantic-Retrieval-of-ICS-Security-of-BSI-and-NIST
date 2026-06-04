create table nist_standard(
    id bigserial primary key,
   
    standard_name text,                               
    source_id text,                     

    section_number text,                
    title text,
    parent text,

    chunk_id text,                      

    content text,
    summary text,

    keywords text[],                   

    lifecycle_phase text,               

    normative boolean,
    normative_type text,                

  
    version text,                      
    year int,                           
    type text                          
);




--create extension vector;

create table requirements_combined (
  id serial primary key,

  -- source
  source_standard text,
  source_id text,
  section_number text,
  chunk_id text,

  -- content
  title text,
  content text,
  summary text,

  -- metadata
  lifecycle_phase text,
  normative boolean,
  normative_type text,
  keywords text,

  abstraction_level text,

  -- embeddings
  embedding vector(384)

);



CREATE TABLE IF NOT EXISTS requirement_mappings (

    id BIGSERIAL PRIMARY KEY,

    source_requirement_id TEXT,

    target_requirement_id TEXT,

    similarity_score FLOAT,

    lifecycle_match BOOLEAN,

    created_at TIMESTAMP DEFAULT NOW()
);