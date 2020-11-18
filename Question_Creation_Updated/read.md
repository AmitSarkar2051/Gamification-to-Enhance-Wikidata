Run the below commands to create a folder of relevant properties:
  1. python3 create_property_generic.py en
  
          (it will extract properties in english, that will be used further to create map file)
  2. python3 create_property_generic.py hi
  
          (to extract properties in hindi we pass argument of hindi language code "hi", for different language you can use different language code)
  3. python3 create_property_map_file_generic.py hi
  
          (this will create map file for hindi language)
  4. python3 extract_members_generic.py hi
  
          (extract all properties and create a folder like "chem_folder_hi", for hindi language)
  
Other codes, 
  (1) to get a mapping file that include automated english to hindi translation we can use the below code with same run cmd,
  create_translation_property_map_file_hi.py 
  run: python3 create_translation_property_map_file_hi.py hi
  
    (note: this code is partially complete as the translation for some properties are not appropriate, and need further verification. So this code is not used in this scope.)
  (2) There is another folder "question_creation" - that contains codes and all relevant files of previous architecture. Those codes support 2 language - Hindi and Bengali. And use static map files.
  
    (note: after the new architecture this is out of scope now.)
