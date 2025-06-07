import os
from neo4j import GraphDatabase, exceptions
from dotenv import load_dotenv

def check_neo4j_connection():
    # Construct the path to the .env file located in the backend directory
    # This assumes the script is run from the project root directory.
    dotenv_path = os.path.join('backend', '.env') 
    
    # Load the .env file from the specified path
    loaded = load_dotenv(dotenv_path=dotenv_path)

    if not loaded:
        print(f"Warning: Could not load .env file from {dotenv_path}")
        print("Please ensure the .env file exists at backend/.env and is readable.")
        # We can still try to load from environment variables if .env file is not found
        # but the original error message implies they were not set in the environment either.

    neo4j_uri = os.getenv("NEO4J_URI")
    neo4j_user = os.getenv("NEO4J_USER")
    neo4j_password = os.getenv("NEO4J_PASSWORD")

    if not all([neo4j_uri, neo4j_user, neo4j_password]):
        print("Error: Missing Neo4j connection details.")
        print("Please ensure NEO4J_URI, NEO4J_USER, and NEO4J_PASSWORD are set, either in")
        print(f"{dotenv_path} or as environment variables.")
        return

    driver = None
    try:
        print(f"Attempting to connect to Neo4j at {neo4j_uri} with user {neo4j_user}...")
        driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        
        driver.verify_connectivity()
        print(f"Successfully connected to Neo4j server at {neo4j_uri}!")

        with driver.session() as session:
            print("Attempting to execute a test query...")
            result = session.run("RETURN 1 AS test_value")
            record = result.single()
            if record and record["test_value"] == 1:
                print("Test query executed successfully. Connection is working!")
            else:
                print("Connected, but test query failed or returned an unexpected result.")
                
    except exceptions.AuthError:
        print(f"Neo4j authentication failed for user '{neo4j_user}'.")
        print(f"Please check your NEO4J_USER and NEO4J_PASSWORD in {dotenv_path} or environment variables.")
    except exceptions.ServiceUnavailable:
        print(f"Neo4j service unavailable at {neo4j_uri}.")
        print("Please ensure the Neo4j server is running and accessible at the specified URI.")
    except exceptions.ConfigurationError as e:
        print(f"Neo4j configuration error: {e}")
        print("This might be due to an invalid URI format or other configuration issues.")
    except Exception as e:
        print(f"An unexpected error occurred while trying to connect to Neo4j: {e}")
    finally:
        if driver:
            driver.close()
            print("Neo4j driver connection closed.")

if __name__ == "__main__":
    check_neo4j_connection()