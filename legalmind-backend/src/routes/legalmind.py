import os
import json
import tempfile
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from openai import OpenAI
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter

legalmind_bp = Blueprint('legalmind', __name__)

# Initialize OpenAI client
client = OpenAI()

# Initialize ChromaDB
vector_db_client = chromadb.PersistentClient(path="./legal_vector_db")
legal_chunks_collection = vector_db_client.get_or_create_collection(name="legal_document_chunks")

# Text splitter for chunking documents
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    is_separator_regex=False,
)

def get_embedding(text, model="text-embedding-ada-002"):
    """Generate embedding for text using OpenAI."""
    text = text.replace("\n", " ")
    response = client.embeddings.create(input=[text], model=model)
    return response.data[0].embedding

def get_llm_response(messages, model="gpt-4"):
    """Get response from LLM."""
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    return response.choices[0].message.content

@legalmind_bp.route('/analyze-document', methods=['POST'])
@cross_origin()
def analyze_document():
    """Analyze a legal document and extract key information."""
    try:
        data = request.get_json()
        document_text = data.get('text', '')
        
        if not document_text:
            return jsonify({'error': 'No document text provided'}), 400
        
        # Extract contract information
        prompt = f"""You are an expert legal assistant. Extract the following information from the provided contract text and return it as a JSON object. If a field is not found, use null.

Expected JSON Schema:
{{
    "parties": [
        {{"name": "string", "role": "string"}}
    ],
    "effective_date": "YYYY-MM-DD or null",
    "termination_date": "YYYY-MM-DD or null",
    "governing_law": "string or null",
    "indemnification_clause": "string or null",
    "confidentiality_clause": "string or null",
    "key_terms": ["list of key terms"],
    "document_type": "string"
}}

Contract Text:
{document_text}

Extracted Information (JSON):
"""
        
        messages = [
            {"role": "system", "content": "You are an expert legal assistant extracting information from contracts. Return only valid JSON."},
            {"role": "user", "content": prompt}
        ]
        
        response = get_llm_response(messages)
        
        try:
            extracted_data = json.loads(response)
        except json.JSONDecodeError:
            # If JSON parsing fails, return a structured error
            extracted_data = {
                "error": "Failed to parse LLM response as JSON",
                "raw_response": response
            }
        
        return jsonify(extracted_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@legalmind_bp.route('/summarize-document', methods=['POST'])
@cross_origin()
def summarize_document():
    """Generate a summary of a legal document."""
    try:
        data = request.get_json()
        document_text = data.get('text', '')
        summary_type = data.get('type', 'concise')  # concise, detailed, key_points
        
        if not document_text:
            return jsonify({'error': 'No document text provided'}), 400
        
        instruction = "Summarize the following legal document. "
        if summary_type == "concise":
            instruction += "Provide a brief, high-level summary, focusing on the main purpose and key outcomes."
        elif summary_type == "detailed":
            instruction += "Provide a detailed summary, covering all major sections and important provisions."
        elif summary_type == "key_points":
            instruction += "Extract the most important key points and present them as a bulleted list."
        
        prompt = f"""{instruction}

Document Text:
{document_text}

Summary:
"""
        
        messages = [
            {"role": "system", "content": "You are a legal summarization expert."},
            {"role": "user", "content": prompt}
        ]
        
        summary = get_llm_response(messages)
        
        return jsonify({'summary': summary, 'type': summary_type})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@legalmind_bp.route('/legal-research', methods=['POST'])
@cross_origin()
def legal_research():
    """Perform legal research using RAG."""
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        if not query:
            return jsonify({'error': 'No query provided'}), 400
        
        # Generate embedding for the query
        query_embedding = get_embedding(query)
        
        # Search vector database
        results = legal_chunks_collection.query(
            query_embeddings=[query_embedding],
            n_results=5,
            include=['documents', 'metadatas']
        )
        
        retrieved_texts = []
        sources = []
        
        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                retrieved_texts.append(doc)
                # Get source info from metadata
                metadata = results['metadatas'][0][i] if results['metadatas'] and results['metadatas'][0] else {}
                source_info = metadata.get('source', f'Document {i+1}')
                sources.append(source_info)
        
        if not retrieved_texts:
            return jsonify({
                'answer': 'I could not find relevant information in the knowledge base to answer your query.',
                'sources': [],
                'query': query
            })
        
        context = "\n\n".join(retrieved_texts)
        
        augmented_prompt = f"""Based on the following legal context, answer the question. Cite the source of each piece of information you use from the context. If you cannot find the answer in the context, state that clearly.

Legal Context:
{context}

Question: {query}

Answer:"""
        
        messages = [
            {"role": "system", "content": "You are a helpful legal assistant that answers questions based on provided context and cites sources."},
            {"role": "user", "content": augmented_prompt}
        ]
        
        answer = get_llm_response(messages)
        
        return jsonify({
            'answer': answer,
            'sources': list(set(sources)),
            'query': query
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@legalmind_bp.route('/draft-document', methods=['POST'])
@cross_origin()
def draft_document():
    """Draft a legal document based on template and parameters."""
    try:
        data = request.get_json()
        document_type = data.get('type', '')
        parameters = data.get('parameters', {})
        
        if not document_type:
            return jsonify({'error': 'No document type provided'}), 400
        
        # Simple NDA template
        if document_type.lower() == 'nda':
            template = """NON-DISCLOSURE AGREEMENT

This Non-Disclosure Agreement ("Agreement") is made and entered into as of {effective_date}, by and between {party_a_name} ("Disclosing Party") and {party_b_name} ("Receiving Party").

WHEREAS, the Disclosing Party possesses certain confidential and proprietary information relating to {confidential_info_description};

NOW, THEREFORE, in consideration of the mutual covenants and agreements contained herein, the parties agree as follows:

1. **Confidential Information.** "Confidential Information" shall mean any and all information disclosed by the Disclosing Party to the Receiving Party, whether orally, visually, or in writing, that is designated as confidential or that reasonably should be understood to be confidential given the nature of the information and the circumstances of disclosure.

2. **Obligations of Receiving Party.** The Receiving Party agrees to use the Confidential Information solely for the purpose of {purpose_of_disclosure} and to protect such information from unauthorized use or disclosure.

3. **Term.** This Agreement shall remain in effect for a period of {term_duration} from the Effective Date.

IN WITNESS WHEREOF, the parties have executed this Agreement as of the Effective Date.

_____________________________
{party_a_name}

_____________________________
{party_b_name}"""
            
            # Fill in the template
            draft = template.format(
                effective_date=parameters.get('effective_date', '[EFFECTIVE_DATE]'),
                party_a_name=parameters.get('party_a_name', '[PARTY_A_NAME]'),
                party_b_name=parameters.get('party_b_name', '[PARTY_B_NAME]'),
                confidential_info_description=parameters.get('confidential_info_description', '[CONFIDENTIAL_INFO_DESCRIPTION]'),
                purpose_of_disclosure=parameters.get('purpose_of_disclosure', '[PURPOSE_OF_DISCLOSURE]'),
                term_duration=parameters.get('term_duration', '[TERM_DURATION]')
            )
            
            # Optional: Use LLM to refine the draft
            refinement_prompt = f"""Review the following legal document draft. Ensure legal coherence, grammatical correctness, and professional tone. Make any necessary minor adjustments without changing the core meaning or structure.

Document Draft:
{draft}

Refined Document:
"""
            
            messages = [
                {"role": "system", "content": "You are a legal document refiner."},
                {"role": "user", "content": refinement_prompt}
            ]
            
            refined_draft = get_llm_response(messages)
            
            return jsonify({
                'draft': refined_draft,
                'document_type': document_type,
                'parameters_used': parameters
            })
        
        else:
            return jsonify({'error': f'Document type "{document_type}" not supported yet'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@legalmind_bp.route('/ingest-sample-data', methods=['POST'])
@cross_origin()
def ingest_sample_data():
    """Ingest sample legal documents into the vector database."""
    try:
        # Sample legal texts for demonstration
        sample_documents = [
            {
                "id": "contract_law_basics",
                "text": """Contract law is a body of law that governs oral and written agreements associated with exchange of goods and services, money, and properties. It includes topics such as the nature of contractual obligations, limitation of actions, freedom of contract, privacy of contract, termination of contract, and covers also agency relationships, commercial paper, and contracts of employment. The essential elements of a contract are: offer, acceptance, consideration, and mutual assent. A contract must also have a lawful purpose and the parties must have legal capacity to enter into the agreement.""",
                "metadata": {"source": "Contract Law Fundamentals", "type": "educational"}
            },
            {
                "id": "force_majeure_definition",
                "text": """Force majeure is a French term that literally means 'greater force.' It refers to a clause that is included in contracts to remove liability for natural and unavoidable catastrophes that interrupt the expected course of events and prevent participants from fulfilling obligations. Force majeure clauses typically cover natural disasters like earthquakes, hurricanes, and floods, as well as human actions such as terrorism, labor strikes, and governmental actions. The specific events covered by a force majeure clause depend on the language of the particular contract.""",
                "metadata": {"source": "Legal Dictionary", "type": "definition"}
            },
            {
                "id": "indemnification_clause",
                "text": """An indemnification clause is a contractual provision in which one party agrees to compensate another party for certain damages, losses, or liabilities. The indemnifying party agrees to hold harmless and defend the indemnified party against claims, lawsuits, damages, and expenses arising from specified circumstances. Indemnification clauses are common in many types of contracts, including service agreements, lease agreements, and purchase agreements. The scope of indemnification can vary widely depending on the specific language used in the clause.""",
                "metadata": {"source": "Contract Clauses Guide", "type": "educational"}
            }
        ]
        
        ingested_count = 0
        
        for doc in sample_documents:
            # Chunk the text
            chunks = text_splitter.split_text(doc["text"])
            
            embeddings = []
            documents = []
            metadatas = []
            ids = []
            
            for i, chunk in enumerate(chunks):
                try:
                    embedding = get_embedding(chunk)
                    embeddings.append(embedding)
                    documents.append(chunk)
                    
                    chunk_metadata = doc["metadata"].copy()
                    chunk_metadata["chunk_id"] = f"{doc['id']}_chunk_{i}"
                    metadatas.append(chunk_metadata)
                    ids.append(f"{doc['id']}_chunk_{i}")
                except Exception as e:
                    print(f"Error generating embedding for chunk {i} of {doc['id']}: {e}")
                    continue
            
            if embeddings:
                legal_chunks_collection.add(
                    embeddings=embeddings,
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
                ingested_count += len(embeddings)
        
        return jsonify({
            'message': f'Successfully ingested {ingested_count} chunks from {len(sample_documents)} documents',
            'documents_processed': len(sample_documents)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@legalmind_bp.route('/health', methods=['GET'])
@cross_origin()
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'service': 'LegalMind AI'})

