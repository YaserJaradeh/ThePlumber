from plumber.api.api import app


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

if __name__ == '__main__':
    print(plumber_logo)
    print("Welcome to Plumber. Pipes never looked this nice before ;)")
    app.run(host='0.0.0.0', port=5000)
    # from plumber.components import *
    # from plumber.discovery import get_classes_map
    # print(len(get_classes_map()))
