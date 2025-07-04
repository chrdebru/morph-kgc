import sys
import os
from rdflib import Graph, BNode, Literal, URIRef, Dataset
from rdflib.compare import isomorphic
import json
import shutil


# Get the absolute path of the directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..', 'src')))

# Import the morph_kgc module from the src folder
import morph_kgc

def test_RMLTC():
    directories = []
    
    # for entry in os.listdir("./rml-cc"):
    #     full_path = os.path.join("./rml-cc", entry)
    #     if os.path.isdir(full_path):
    #         directories.append(entry)

    directories = [
        "RMLTC-CC-0001-Alt",
        "RMLTC-CC-0001-Bag",
        "RMLTC-CC-0001-List",
        "RMLTC-CC-0001-Seq",
        "RMLTC-CC-0002-Bag",
        "RMLTC-CC-0002-List",
        "RMLTC-CC-0003-EB",
        "RMLTC-CC-0003-EL",
        "RMLTC-CC-0003-EL-BN",
        "RMLTC-CC-0003-EL-Named",
        "RMLTC-CC-0003-NEB",
        "RMLTC-CC-0003-NEL",
        "RMLTC-CC-0003-NELb",
        "RMLTC-CC-0004-SM1",
        "RMLTC-CC-0004-SM2",
        "RMLTC-CC-0004-SM3",
        "RMLTC-CC-0004-SM4",
        "RMLTC-CC-0004-SM5",
        "RMLTC-CC-0005-App1",
        "RMLTC-CC-0005-App2",
        "RMLTC-CC-0005-Car1",
        "RMLTC-CC-0005-Car2",
        "RMLTC-CC-0006-IT0",
        "RMLTC-CC-0006-IT1",
        "RMLTC-CC-0006-IT2",
        "RMLTC-CC-0006-IT3",
        "RMLTC-CC-0006-IT4",
        "RMLTC-CC-0006-IT5",
        "RMLTC-CC-0007-NES",
        "RMLTC-CC-0008-ROMa",
        "RMLTC-CC-0008-ROMb",
        "RMLTC-CC-0009-DUP-Bag",
        "RMLTC-CC-0009-DUP-List"
    ]

    dictionary = dict()
    for entry in directories:
        dictionary[entry] = False

    for tc in directories:
        print(f"Running test case: {tc}")

        try:
            mapping_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'rml-cc', tc, 'mapping.ttl')
            default_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'rml-cc', tc, 'default.nq')
            
            try:
                data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'rml-cc', tc, 'data.json')
                data_local_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data.json')
                shutil.copy(data_path, data_local_path)
            except Exception as e:
                print(f"Error copying data file for test case {tc}: {e}")

            try:
                student_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'rml-cc', tc, 'student.csv')
                student_path_local = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'student.csv')
                shutil.copy(student_path, student_path_local)
            except Exception as e:
                print(f"Error copying data file for test case {tc}: {e}")

            # Config file
            config = f'[CONFIGURATION]\noutput_format=N-QUADS\n[DataSource]\nmappings={mapping_path}'

            # Generation of triples from mapping
            triples = morph_kgc.materialize(config)

            # Load the expected triples into a graph   
            g = Graph()
            g.parse(default_path)

            dictionary[tc] = isomorphic(g, triples)

            if not isomorphic(g, triples):
                print(triples.serialize(format="turtle"))
                print("---")
                print(g.serialize(format="turtle"))

        except Exception as e:
            print(f"Error processing test case {tc}: {e}")
            print(e)
            continue

    # NEED TO BE TESTED MANUALLY
    directories = [ "RMLTC-CC-0010-List", "RMLTC-CC-0010-Listb" ]
    for entry in directories:
        dictionary[entry] = False

    for tc in directories:
        print(f"Running test case: {tc}")

        try:
            mapping_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'rml-cc', tc, 'mapping.ttl')
            default_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'rml-cc', tc, 'default.nq')
            
            try:
                data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'rml-cc', tc, 'data.json')
                data_local_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data.json')
                shutil.copy(data_path, data_local_path)
            except Exception as e:
                print(f"Error copying data file for test case {tc}: {e}")

            # Config file
            config = f'[CONFIGURATION]\noutput_format=N-QUADS\n[DataSource]\nmappings={mapping_path}'

            # Generation of triples from mapping
            triples = morph_kgc.materialize_set(config)
            
            # Load the expected triples into a graph   
            g = Dataset()
            g.parse(default_path)

            #dictionary[tc] = are_datasets_structurally_isomorphic(g, triples)

            for t in triples:
                print(t)
            print("---")
            print(g.serialize(format="trig"))

        except Exception as e:
            print(f"Error processing test case {tc}: {e}")
            print(e)
            continue

    print(json.dumps(dictionary, indent=2, sort_keys=True))


def are_datasets_structurally_isomorphic(dataset1: Dataset, dataset2: Dataset) -> bool:
    contexts1 = sorted([str(c) for c in dataset1.contexts()]) # Convert to string for simple comparison
    contexts2 = sorted([str(c) for c in dataset2.contexts()])

    # Basic check: do they have the same number of named graphs?
    if len(contexts1) != len(contexts2):
        print("Number of contexts differs.")
        return False

    # If contexts are URIs, you can do a direct comparison or mapping
    # If contexts are blank nodes, this becomes much harder and requires a BNode mapping algorithm

    # For simplicity, assuming named contexts match or are consistent
    # This part needs careful design for real-world scenarios with blank node contexts
    # For this example, let's assume they map directly or we normalize identifiers
    # This is a very simplified check that assumes direct URI correspondence or simple relabelling
    # A robust solution would involve a more sophisticated graph matching algorithm.

    # Create a mapping for context URIs if they are different but conceptually match
    # For instance, if ds1 has contextA and ds2 has contextB, and they represent the same structure
    # This is out of scope for a simple example.

    # Let's just compare the default graph and see if the named graphs match by string of URI
    g1_default = dataset1.default_context
    g2_default = dataset2.default_context
    if not g1_default.is_isomorphic(g2_default):
        print("Default graphs are not isomorphic.")
        return False

    # Build a mapping from context ID in ds1 to context ID in ds2 if possible
    # This is the hardest part. For now, we'll assume exact URI match for named graphs
    named_graphs1_map = {str(c): dataset1.get_context(c) for c in dataset1.contexts() if c != dataset1.default_context.identifier}
    named_graphs2_map = {str(c): dataset2.get_context(c) for c in dataset2.contexts() if c != dataset2.default_context.identifier}

    if set(named_graphs1_map.keys()) != set(named_graphs2_map.keys()):
        print("Named graph identifiers differ.")
        return False

    for context_uri in named_graphs1_map:
        if not named_graphs1_map[context_uri].is_isomorphic(named_graphs2_map[context_uri]):
            print(f"Named graph {context_uri} is not isomorphic.")
            return False

    return True

if __name__ == "__main__":
    test_RMLTC()
