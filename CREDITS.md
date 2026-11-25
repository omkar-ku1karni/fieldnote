# Credits

## Models

| Role | Model | License |
|---|---|---|
| Page retrieval | `vidore/colSmol-256M` | MIT |
| Photo retrieval | `google/siglip2-so400m-patch14-384` | Apache-2.0 |
| Text retrieval | `BAAI/bge-base-en-v1.5` | MIT |
| Reranker (ablation) | `cross-encoder/ms-marco-MiniLM-L6-v2` | Apache-2.0 |
| Reranker (ablation) | `BAAI/bge-reranker-base` | MIT |
| Speech recognition | `Systran/faster-whisper-small.en (OpenAI Whisper)` | MIT |
| Call audio (text-to-speech) | `hexgrad/Kokoro-82M` | Apache-2.0 |

Answer generation uses a hosted model (Gemini or Groq) when keys are set, or a local Ollama model otherwise; no model weights are redistributed by this repo.

## Job-site photos

Downloaded from Wikimedia Commons at build time (`make photos`); this repository does not store them. Each photo was resized and stripped of EXIF metadata. Fictional job metadata (site, unit, date, technician) is attached by `datagen/photos.py`; it does not describe the real photo.

| Photo id | Title | Author | License |
|---|---|---|---|
| P-LMOB-RTU7-01 | [Exploded capacitor (5201542058).jpg](https://commons.wikimedia.org/wiki/File:Exploded_capacitor_(5201542058).jpg) | Marco d'Itri from Milano, Italy | [CC BY-SA 2.0](https://creativecommons.org/licenses/by-sa/2.0) |
| P-HPDC-RTU4-01 | [Dirty AC filters 2023 (1) 01.jpg](https://commons.wikimedia.org/wiki/File:Dirty_AC_filters_2023_(1)_01.jpg) | Gerardolagunes | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) |
| P-BES-RTU4-01 | [Ilmalämpöpumppu (2 of 3).jpg](https://commons.wikimedia.org/wiki/File:Ilmal%C3%A4mp%C3%B6pumppu_(2_of_3).jpg) | Kuvatusmedia | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0) |
| P-NFC-RTU3-01 | [Burned Contactor-01ASD.jpg](https://commons.wikimedia.org/wiki/File:Burned_Contactor-01ASD.jpg) | Asurnipal | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) |
| P-004 | [Motor-Start-Capacitor.jpg](https://commons.wikimedia.org/wiki/File:Motor-Start-Capacitor.jpg) | Elcap | [CC0](http://creativecommons.org/publicdomain/zero/1.0/deed.en) |
| P-005 | [Shugart SA1004 HDD - AC motor and run capacitor.jpg](https://commons.wikimedia.org/wiki/File:Shugart_SA1004_HDD_-_AC_motor_and_run_capacitor.jpg) | Mister rf | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) |
| P-006 | [Heat exchanger at DEQ IST.jpg](https://commons.wikimedia.org/wiki/File:Heat_exchanger_at_DEQ_IST.jpg) | Organic sweet | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) |
| P-007 | [Shell and Tube Heat Exchanger Piping 1.jpg](https://commons.wikimedia.org/wiki/File:Shell_and_Tube_Heat_Exchanger_Piping_1.jpg) | Ivangiesen | [CC0](http://creativecommons.org/publicdomain/zero/1.0/deed.en) |
| P-008 | [Shell and Tube Heat Exchanger of Chiller.jpg](https://commons.wikimedia.org/wiki/File:Shell_and_Tube_Heat_Exchanger_of_Chiller.jpg) | Saud | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) |
| P-009 | [Aging Condenser Unit of a Split Air Conditioning System (7547606426).jpg](https://commons.wikimedia.org/wiki/File:Aging_Condenser_Unit_of_a_Split_Air_Conditioning_System_(7547606426).jpg) | Chris Hunkeler from Carlsbad, California, USA | [CC BY-SA 2.0](https://creativecommons.org/licenses/by-sa/2.0) |
| P-010 | [Air Conditioning Units circa 1995.JPG](https://commons.wikimedia.org/wiki/File:Air_Conditioning_Units_circa_1995.JPG) | JoeBensonAC | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) |
| P-011 | [Air Conditioning units on the roof, hospital building, 2021, 03.jpg](https://commons.wikimedia.org/wiki/File:Air_Conditioning_units_on_the_roof,_hospital_building,_2021,_03.jpg) | Kgbo | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) |
| P-012 | [Air conditioners in Nis.jpg](https://commons.wikimedia.org/wiki/File:Air_conditioners_in_Nis.jpg) | Tiia Monto | [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0) |
| P-013 | [BRP Humabon - Air Conditioning Condenser.jpg](https://commons.wikimedia.org/wiki/File:BRP_Humabon_-_Air_Conditioning_Condenser.jpg) | Rhk111 | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) |
| P-014 | [Condenser unit for central air conditioning.JPG](https://commons.wikimedia.org/wiki/File:Condenser_unit_for_central_air_conditioning.JPG) | H Padleckas | [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0) |
| P-015 | [Industrial air conditioning unit (DFdB).JPG](https://commons.wikimedia.org/wiki/File:Industrial_air_conditioning_unit_(DFdB).JPG) | Dein Freund der Baum | [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0) |
| P-016 | [Marstair air conditioning condenser unit mounted on red plastered wall, 1 Ingram Road, Gillingham, Kent, England.jpg](https://commons.wikimedia.org/wiki/File:Marstair_air_conditioning_condenser_unit_mounted_on_red_plastered_wall,_1_Ingram_Road,_Gillingham,_Kent,_England.jpg) | OathOn | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) |
| P-017 | [SHARP air conditioner outdoor unit 20201003.jpg](https://commons.wikimedia.org/wiki/File:SHARP_air_conditioner_outdoor_unit_20201003.jpg) | 円周率３パーセント | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) |
| P-018 | [Snow covers an outdoor air conditioning unit in a winter landscape during a heavy snowfall.jpg](https://commons.wikimedia.org/wiki/File:Snow_covers_an_outdoor_air_conditioning_unit_in_a_winter_landscape_during_a_heavy_snowfall.jpg) | Shixart1985 | [CC BY 2.0](https://creativecommons.org/licenses/by/2.0) |
| P-019 | [Air conditioner, Sofia (P1070790).jpg](https://commons.wikimedia.org/wiki/File:Air_conditioner,_Sofia_(P1070790).jpg) | Matti Blume | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) |
| P-020 | [HVAC.jpg](https://commons.wikimedia.org/wiki/File:HVAC.jpg) | National Institute of Standards and Technology | Public domain |
| P-021 | [Panasonic CONDENSING UNIT OCU-NR200SF-D.jpg](https://commons.wikimedia.org/wiki/File:Panasonic_CONDENSING_UNIT_OCU-NR200SF-D.jpg) | Dinkun Chen | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) |
| P-022 | [Panasonic CONDENSING UNIT OCU-NS500HF.jpg](https://commons.wikimedia.org/wiki/File:Panasonic_CONDENSING_UNIT_OCU-NS500HF.jpg) | Dinkun Chen | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) |
| P-023 | [Panasonic CONDENSING UNIT OCU-S700HF.jpg](https://commons.wikimedia.org/wiki/File:Panasonic_CONDENSING_UNIT_OCU-S700HF.jpg) | Dinkun Chen | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) |
| P-024 | [Refrigeration Compressors for the Altitude Wind Tunnel (GRC-1944-C-06715).jpg](https://commons.wikimedia.org/wiki/File:Refrigeration_Compressors_for_the_Altitude_Wind_Tunnel_(GRC-1944-C-06715).jpg) | NASA Glenn Research Center | Public domain |
| P-025 | [Gree Ease Wind air conditioner.jpg](https://commons.wikimedia.org/wiki/File:Gree_Ease_Wind_air_conditioner.jpg) | Fumikas Sagisavas | [CC0](http://creativecommons.org/publicdomain/zero/1.0/deed.en) |
| P-026 | [Rooftop Packaged Units.JPG](https://commons.wikimedia.org/wiki/File:Rooftop_Packaged_Units.JPG) | P199 | Public domain |
| P-027 | [012 Rooftop HVAC systems and roof ventilation ducts in Tokyo, Japan.jpg](https://commons.wikimedia.org/wiki/File:012_Rooftop_HVAC_systems_and_roof_ventilation_ducts_in_Tokyo,_Japan.jpg) | Marek Ślusarczyk (Tupungato) Photo portfolio | [CC BY 3.0](https://creativecommons.org/licenses/by/3.0) |
| P-028 | [013 Office building air conditioning rooftop system in Tokyo city - airconditioning op het dak.jpg](https://commons.wikimedia.org/wiki/File:013_Office_building_air_conditioning_rooftop_system_in_Tokyo_city_-_airconditioning_op_het_dak.jpg) | Marek Ślusarczyk (Tupungato) Photo portfolio | [CC BY 3.0](https://creativecommons.org/licenses/by/3.0) |
| P-029 | [130420-F-ZZ999-101 (15718415681), rooftop HVAC.jpg](https://commons.wikimedia.org/wiki/File:130420-F-ZZ999-101_(15718415681),_rooftop_HVAC.jpg) | Los Angeles Air Force Base Space and Missile System Center | Public domain |
| P-030 | [Air conditioning office building roof - public building air conditioning in Tokyo.jpg](https://commons.wikimedia.org/wiki/File:Air_conditioning_office_building_roof_-_public_building_air_conditioning_in_Tokyo.jpg) | Marek Ślusarczyk (Tupungato) Photo portfolio | [CC BY 3.0](https://creativecommons.org/licenses/by/3.0) |
| P-031 | [Helicopter delivering a rooftop HVAC unit -04- (9721469418).jpg](https://commons.wikimedia.org/wiki/File:Helicopter_delivering_a_rooftop_HVAC_unit_-04-_(9721469418).jpg) | Ben Schumin from Montgomery Village, Maryland, USA | [CC BY-SA 2.0](https://creativecommons.org/licenses/by-sa/2.0) |
| P-032 | [23 0041077 Convair Negative Image - Motor compressor and air conditioner (53718436726).jpg](https://commons.wikimedia.org/wiki/File:23_0041077_Convair_Negative_Image_-_Motor_compressor_and_air_conditioner_(53718436726).jpg) | San Diego Air &amp; Space Museum Archives | Public domain |
| P-033 | [BURNED OUT AIR CONDITIONER AND COMPRESSOR AND COIL - NARA - 17441993.jpg](https://commons.wikimedia.org/wiki/File:BURNED_OUT_AIR_CONDITIONER_AND_COMPRESSOR_AND_COIL_-_NARA_-_17441993.jpg) | Unknown authorUnknown author or not provided | Public domain |
| P-034 | [MHI AC COMPRESSOR (Minica H42V).jpg](https://commons.wikimedia.org/wiki/File:MHI_AC_COMPRESSOR_(Minica_H42V).jpg) | Hd207 | [CC0](http://creativecommons.org/publicdomain/zero/1.0/deed.en) |
| P-035 | [Panasonic AIR CONDITIONER COMPRESSOR 2P15S225CZB.jpg](https://commons.wikimedia.org/wiki/File:Panasonic_AIR_CONDITIONER_COMPRESSOR_2P15S225CZB.jpg) | Dinkun Chen | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) |
| P-036 | [Electric Vehicle Scroll Compressor.jpg](https://commons.wikimedia.org/wiki/File:Electric_Vehicle_Scroll_Compressor.jpg) | R2T2M | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) |
| P-037 | [Scroll Compressor.jpeg](https://commons.wikimedia.org/wiki/File:Scroll_Compressor.jpeg) | Kludge2 | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) |
| P-038 | [Air Handler Unit aanzuiging.JPG](https://commons.wikimedia.org/wiki/File:Air_Handler_Unit_aanzuiging.JPG) | Alf van Beem | [CC0](http://creativecommons.org/publicdomain/zero/1.0/deed.en) |
| P-039 | [Air handling unit.JPG](https://commons.wikimedia.org/wiki/File:Air_handling_unit.JPG) | P199 | Public domain |
| P-040 | [Air handling units in large commercial building, Brisbane.jpg](https://commons.wikimedia.org/wiki/File:Air_handling_units_in_large_commercial_building,_Brisbane.jpg) | Kgbo | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) |
| P-041 | [Air handling units in large commercial building, Brisbane 01.jpg](https://commons.wikimedia.org/wiki/File:Air_handling_units_in_large_commercial_building,_Brisbane_01.jpg) | Kgbo | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) |
| P-042 | [HVAC Air Handler Unit, pic1.JPG](https://commons.wikimedia.org/wiki/File:HVAC_Air_Handler_Unit,_pic1.JPG) | Alf van Beem | [CC0](http://creativecommons.org/publicdomain/zero/1.0/deed.en) |
| P-043 | [HVAC Air Handler Unit, pic2.JPG](https://commons.wikimedia.org/wiki/File:HVAC_Air_Handler_Unit,_pic2.JPG) | Alf van Beem | [CC0](http://creativecommons.org/publicdomain/zero/1.0/deed.en) |
| P-044 | [HVAC Air Handler Unit, pic3.JPG](https://commons.wikimedia.org/wiki/File:HVAC_Air_Handler_Unit,_pic3.JPG) | Alf van Beem | [CC0](http://creativecommons.org/publicdomain/zero/1.0/deed.en) |
| P-045 | [Mitsubishi Heat Pump interior air handler.agr.jpg](https://commons.wikimedia.org/wiki/File:Mitsubishi_Heat_Pump_interior_air_handler.agr.jpg) | ArnoldReinhold | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) |
| P-046 | [Aardgasfornuisvlam.jpg](https://commons.wikimedia.org/wiki/File:Aardgasfornuisvlam.jpg) | Sapp | Public domain |
| P-047 | [332nd Expeditionary CE Squadron HVAC-R operations (9305716).jpg](https://commons.wikimedia.org/wiki/File:332nd_Expeditionary_CE_Squadron_HVAC-R_operations_(9305716).jpg) | U.S. Air Force AFCENT by Senior Airman Grace Turpin | Public domain |
| P-048 | [Cool under pressure- 386th ECES HVAC technicians in action (9047740).jpg](https://commons.wikimedia.org/wiki/File:Cool_under_pressure-_386th_ECES_HVAC_technicians_in_action_(9047740).jpg) | U.S. Air Force photo by Senior Airman Mark Colmenares | Public domain |
| P-049 | [379th ECES HVAC technicians combat rising temperatures (8502255).jpg](https://commons.wikimedia.org/wiki/File:379th_ECES_HVAC_technicians_combat_rising_temperatures_(8502255).jpg) | U.S. Air Force AFCENT by Airman 1st Class Derrick Bole | Public domain |
| P-050 | [379th ECES HVAC technicians combat rising temperatures (8502257).jpg](https://commons.wikimedia.org/wiki/File:379th_ECES_HVAC_technicians_combat_rising_temperatures_(8502257).jpg) | U.S. Air Force AFCENT by Airman 1st Class Derrick Bole | Public domain |
| P-051 | [379th ECES HVAC technicians combat rising temperatures (8502258).jpg](https://commons.wikimedia.org/wiki/File:379th_ECES_HVAC_technicians_combat_rising_temperatures_(8502258).jpg) | U.S. Air Force AFCENT by Airman 1st Class Derrick Bole | Public domain |
| P-052 | [379th ECES HVAC technicians combat rising temperatures (8502259).jpg](https://commons.wikimedia.org/wiki/File:379th_ECES_HVAC_technicians_combat_rising_temperatures_(8502259).jpg) | U.S. Air Force AFCENT by Airman 1st Class Derrick Bole | Public domain |
| P-053 | [HVAC Technicians Power Mission Success (8850027).jpg](https://commons.wikimedia.org/wiki/File:HVAC_Technicians_Power_Mission_Success_(8850027).jpg) | U.S. Air Force photo by Airman 1st Class Skylar Ellis | Public domain |
| P-054 | [HVAC Technicians Power Mission Success (8850029).jpg](https://commons.wikimedia.org/wiki/File:HVAC_Technicians_Power_Mission_Success_(8850029).jpg) | U.S. Air Force photo by Airman 1st Class Skylar Ellis | Public domain |
| P-055 | [HVAC Technicians Power Mission Success (8850032).jpg](https://commons.wikimedia.org/wiki/File:HVAC_Technicians_Power_Mission_Success_(8850032).jpg) | U.S. Air Force photo by Airman 1st Class Skylar Ellis | Public domain |
| P-056 | [HVAC Technicians Power Mission Success (8850033).jpg](https://commons.wikimedia.org/wiki/File:HVAC_Technicians_Power_Mission_Success_(8850033).jpg) | U.S. Air Force photo by Airman 1st Class Skylar Ellis | Public domain |
| P-057 | [McQuay AIR CONDITIONING AIR CONDITIONER OUTDOOR UNIT.jpg](https://commons.wikimedia.org/wiki/File:McQuay_AIR_CONDITIONING_AIR_CONDITIONER_OUTDOOR_UNIT.jpg) | Dinkun Chen | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) |
| P-058 | [BLOWER INLET AND WHEEL AT LASER LABORATORY - NARA - 17441823.jpg](https://commons.wikimedia.org/wiki/File:BLOWER_INLET_AND_WHEEL_AT_LASER_LABORATORY_-_NARA_-_17441823.jpg) | Martin Brown | Public domain |
| P-059 | [BLOWER INLET AND WHEEL AT LASER LABORATORY - NARA - 17441824.jpg](https://commons.wikimedia.org/wiki/File:BLOWER_INLET_AND_WHEEL_AT_LASER_LABORATORY_-_NARA_-_17441824.jpg) | Martin Brown | Public domain |
| P-060 | [Destroyer, plan of machinery and boiler rooms (Warships To-day, 1936).jpg](https://commons.wikimedia.org/wiki/File:Destroyer,_plan_of_machinery_and_boiler_rooms_(Warships_To-day,_1936).jpg) | Andy Dingley (scanner) | Public domain |
| P-061 | [A dirty cabin filter.jpg](https://commons.wikimedia.org/wiki/File:A_dirty_cabin_filter.jpg) | UnifiedFunctionality | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) |
| P-062 | [Dirty-air-filter.jpg](https://commons.wikimedia.org/wiki/File:Dirty-air-filter.jpg) | Ahanix1989 at English Wikipedia | Public domain |
| P-063 | [Dirty AC filters 2023 (1) 02.jpg](https://commons.wikimedia.org/wiki/File:Dirty_AC_filters_2023_(1)_02.jpg) | Gerardolagunes | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) |
| P-064 | [Dirty AC filters 2023 (1) 03.jpg](https://commons.wikimedia.org/wiki/File:Dirty_AC_filters_2023_(1)_03.jpg) | Gerardolagunes | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) |
| P-065 | [Dirty AC filters 2023 (1) 04.jpg](https://commons.wikimedia.org/wiki/File:Dirty_AC_filters_2023_(1)_04.jpg) | Gerardolagunes | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) |
| P-066 | [Dirty Jobs- RAF Fairford edition (9851636).jpg](https://commons.wikimedia.org/wiki/File:Dirty_Jobs-_RAF_Fairford_edition_(9851636).jpg) | U.S. Air Force photo by Senior Airman Adam Enbal | Public domain |
| P-067 | [Dirty Jobs- RAF Fairford edition (9851641).jpg](https://commons.wikimedia.org/wiki/File:Dirty_Jobs-_RAF_Fairford_edition_(9851641).jpg) | U.S. Air Force 501CSW by Senior Airman Adam Enbal | Public domain |
| P-068 | [378th ECES Airmen Maintain HVAC Equipment (8720241).jpg](https://commons.wikimedia.org/wiki/File:378th_ECES_Airmen_Maintain_HVAC_Equipment_(8720241).jpg) | U.S. Air Force AFCENT by Staff Sgt. Shaei Rodriguez | Public domain |
| P-069 | [Ecodan outdoor unit Internal view.jpg](https://commons.wikimedia.org/wiki/File:Ecodan_outdoor_unit_Internal_view.jpg) | PeterEastern | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) |
| P-070 | [Ecodan outdoor unit in the snow.jpg](https://commons.wikimedia.org/wiki/File:Ecodan_outdoor_unit_in_the_snow.jpg) | PeterEastern | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) |
| P-071 | [Outdoor air conditioner unit installed in residential garden space.jpg](https://commons.wikimedia.org/wiki/File:Outdoor_air_conditioner_unit_installed_in_residential_garden_space.jpg) | Shixart1985 | [CC BY 2.0](https://creativecommons.org/licenses/by/2.0) |
| P-072 | [Air duct pipes in Torp shopping mall, Uddevalla.jpg](https://commons.wikimedia.org/wiki/File:Air_duct_pipes_in_Torp_shopping_mall,_Uddevalla.jpg) | W.carter | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) |
| P-073 | [Insulated duct 1.jpg](https://commons.wikimedia.org/wiki/File:Insulated_duct_1.jpg) | Achim Hering | [CC BY 3.0](https://creativecommons.org/licenses/by/3.0) |
| P-074 | [Insulated duct 2.jpg](https://commons.wikimedia.org/wiki/File:Insulated_duct_2.jpg) | Achim Hering | [CC BY 3.0](https://creativecommons.org/licenses/by/3.0) |
| P-075 | [OC Fairground HVAC vent.jpg](https://commons.wikimedia.org/wiki/File:OC_Fairground_HVAC_vent.jpg) | Eric Polk | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) |
| P-076 | [OC Fairground ductwork.jpg](https://commons.wikimedia.org/wiki/File:OC_Fairground_ductwork.jpg) | Eric Polk | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) |
| P-077 | [Office building infrastructure.jpg](https://commons.wikimedia.org/wiki/File:Office_building_infrastructure.jpg) | Eric Polk | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) |
| P-078 | [Contactor DIN IEK.jpg](https://commons.wikimedia.org/wiki/File:Contactor_DIN_IEK.jpg) | Kae | [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0) |
| P-079 | [Moscow trolleybus ZiU-10 2656 2005-03 1110906829.jpg](https://commons.wikimedia.org/wiki/File:Moscow_trolleybus_ZiU-10_2656_2005-03_1110906829.jpg) | Artyom Svetlov | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) |
| P-080 | [Electrical fire damage.jpg](https://commons.wikimedia.org/wiki/File:Electrical_fire_damage.jpg) | "craignoble666" | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) |
| P-081 | [SAFETY RULE №1 - REMOVE THE VOLTAGE BEFORE ANY ACTION AT ELECTRICAL WIRING.JPG](https://commons.wikimedia.org/wiki/File:SAFETY_RULE_%E2%84%961_-_REMOVE_THE_VOLTAGE_BEFORE_ANY_ACTION_AT_ELECTRICAL_WIRING.JPG) | Dmitry G | [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0) |
| P-082 | [Specialized aviation maintainers repair damaged helicopter's electrical system in painstaking project 131117-A-TP284-001.jpg](https://commons.wikimedia.org/wiki/File:Specialized_aviation_maintainers_repair_damaged_helicopter%27s_electrical_system_in_painstaking_project_131117-A-TP284-001.jpg) | Staff Sgt. Todd Pouliot | Public domain |
| P-083 | [Specialized aviation maintainers repair damaged helicopter’s electrical system in painstaking project 131117-A-TP284-002.jpg](https://commons.wikimedia.org/wiki/File:Specialized_aviation_maintainers_repair_damaged_helicopter%E2%80%99s_electrical_system_in_painstaking_project_131117-A-TP284-002.jpg) | Staff Sgt. Todd Pouliot | Public domain |
| P-084 | [Panasonic AIR CONDITIONER COMPRESSOR 2K22S225BUA.jpg](https://commons.wikimedia.org/wiki/File:Panasonic_AIR_CONDITIONER_COMPRESSOR_2K22S225BUA.jpg) | Dinkun Chen | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) |
| P-085 | [Cool under pressure- 386th ECES HVAC technicians in action (9047739).jpg](https://commons.wikimedia.org/wiki/File:Cool_under_pressure-_386th_ECES_HVAC_technicians_in_action_(9047739).jpg) | U.S. Air Force photo by Senior Airman Mark Colmenares | Public domain |

## Everything else

Vantorr Climate Systems, Ridgeline Mechanical Services, every site, unit, person and part number are fictional. Manuals, bulletins and call scripts were written for this project (prose by an LLM from facts in `datagen/world.py`; figures, register and audio generated by code).
