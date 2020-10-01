
plumber_logo = """                (/                                   (/               
     /////////////./////////////////////////////////.////////////,    
   /////////////(/./////////////////////////////////.///////////////  
 .///////                                                     /////// 
 //////                                /*                       //////
 /////                              ///                          /////
 ////////                           ///      /                   /////
(///////////                        //////////                   /////
 ///////(///(//*                  //////  ,                      /////
 //////////////////             /////.                           /////
 ///////////////(//////////////////.                             /////
 /////////////////////////////////                               /////
 /////      ////(//////////////////                              /////
 /////          ,//////////////////                              /////
 /////            ///////////////.     /////////(//////,         /////
 /////             ////////////              ////                /////
 /(///              (//* ,//       *       /(//////              /(///
 /////                       ////// //*////////////////,//////////////
 /////                       ////// //*////////////////,//////////////
 /////                       ////// //*////////////////,//////////////
 /////                              //                  ///      /////
(/////                                                           /////
 /////                                                           /////
 /////                                                           /////
 //////                                                         //////
  ///////                                                     /////// 
   /////////////(/////////////////////////////////// ///////////////  
     ,////////////////////////////////////////////// ////////////,    
"""
from pipeline.pipeline_manager import * 

if __name__ == '__main__':
    print(plumber_logo)
    print("Welcome to Plumber. Pipes never looked this nice before ;)")
    # from plumber.components import *
    # from plumber.discovery import get_classes_map
    # print(len(get_classes_map()))

    # resources = ["R12220", "R12223", "R12226", "R12231", "R12233", \
    #     "R12235", "R12237", "R12241", "R12243", "R12245", "R12247", "R25005", "R36109", \
    #         "R36114", "R36123", "R36138", "R36151", "R37001", "R37003", "R37006", "R37008"]

    resources = ["R36138"]

    config = {
        "pipeline": {
            "name": "test",
            "components": {
                "extractor": "user",
                "linker": "dummy",
                "resolver": "dummy",
                "reader": "raw_file",
                "writer": "file"
            },
            "parameters": {
                "input_file": 'plumber\data\R36138.txt',
                "output_file": 'plumber\data\R36138-triples.txt'
            }
        }
    }
    for resource in resources:
        config["pipeline"]["parameters"]["input_file"] = f"plumber/data/{resource}.txt"
        config["pipeline"]["parameters"]["output_file"] = f"plumber/data/{resource}-triples.txt"
        pipeline, params = PipelineParser.create(config)
        pipeline.consume([1])
        # PipelineParser.clean_up(params)