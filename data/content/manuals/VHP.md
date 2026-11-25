# Vantorr VHP Series Packaged Rooftop Heat Pump — Installation, Operation and Maintenance Manual
<!-- doc_id: VHP-IOM | revision: C | date: 2024-02 -->

## 1. Safety considerations

### 1.1 Scope and responsibilities

This manual provides installation, startup, operating, service, and maintenance instructions for Vantorr VHP Series packaged rooftop heat pumps, models VHP-036, VHP-048, and VHP-060. Each unit uses a single-stage scroll compressor, an R-454B refrigeration circuit, and a VCB-210 control board. The information applies to field work on the complete rooftop assembly, including the indoor air path, outdoor coil section, condensate handling, controls, electrical equipment, and refrigerant detection system.

Installation and service must be performed by personnel qualified for electrical work, refrigeration service, rooftop access, and handling A2L refrigerants. Read the complete manual before beginning work. Retain it near the equipment and make its instructions available to the owner and subsequent service personnel. Verify the actual unit model and electrical configuration against its rating plate before ordering materials or connecting power. Site requirements and applicable codes take precedence wherever they impose additional protections.

> **WARNING:** ELECTRICAL SHOCK, FIRE, AND MOVING-PART HAZARD. Disconnect and lock out every electrical power source before opening an electrical compartment or placing hands near fans, belts, or rotating assemblies. Verify absence of voltage with an appropriately rated instrument. A thermostat set to OFF is not a power disconnect.

> **WARNING:** FALL AND CRUSH HAZARD. Use approved roof access, fall protection, rigging equipment, and a lifting plan appropriate for the installed unit. Keep personnel clear of suspended equipment and the roof opening. Never use cabinet panels, refrigerant lines, or service connections as lifting points.

### 1.2 Signal words and safe work practices

WARNING identifies a condition that could cause death or serious injury. CAUTION identifies a condition that could damage equipment or cause minor injury. NOTE identifies information important for correct installation, operation, or diagnosis. Follow all three types of notice. Use appropriate personal protective equipment for sharp sheet-metal edges, hot surfaces, rotating equipment, pressurized refrigerant, and roof conditions.

Only use replacement materials and components appropriate for the application and refrigerant classification. Do not alter factory-installed protective circuits, defeat safety switches, or substitute a thermostat for an electrical disconnect. If a protective device repeatedly interrupts operation, identify the underlying cause rather than forcing another operating cycle.

### 1.3 R-454B and A2L refrigerant precautions

R-454B is an A2L refrigerant with lower flammability. A release can create a flammable atmosphere under certain conditions. A2L handling requirements apply during installation, leak investigation, evacuation, recovery, repair, charging, and disposal. The presence of a refrigerant detection system does not remove the technician's obligation to follow safe refrigerant practices.

> **WARNING:** A2L REFRIGERANT HAZARD. Eliminate open flames, sparks, smoking, and other ignition sources before opening the refrigerant circuit or investigating a suspected leak. Use equipment, leak-detection methods, and service procedures suitable for R-454B and its A2L classification. Do not use air or oxygen for pressure testing.

Establish ventilation appropriate to the work area and applicable requirements. Inspect the work location for potential ignition sources before using leak-search equipment or removing sealed components. Confirm that recovery equipment, cylinders, gauges, hoses, and instruments are approved for the refrigerant being handled. Follow the recovery device and cylinder instructions; do not discharge refrigerant into the atmosphere. Identify recovered refrigerant so it is not mixed with incompatible refrigerants.

A suspected leak requires a controlled response. Stop work that could produce ignition, follow the site's emergency procedures, assess the area with appropriate instruments, and isolate power only when it is safe to do so. Do not energize suspect electrical equipment to locate a leak. The factory refrigerant detection system is a protective feature, not a substitute for a technician's independent leak check. Section 14 describes the required inspection and service approach.

> **CAUTION:** Never introduce R-410A or any other refrigerant into a VHP unit. Use the refrigerant specified on the VHP rating plate. An incorrect refrigerant or contaminated charge may damage the equipment and create a safety hazard.

### 1.4 Pressure, temperature, and mechanical hazards

A refrigeration circuit can remain pressurized when power is removed. Use appropriate recovery and isolation procedures before loosening tubing, pressure taps, or service components. Verify that the circuit is safe to open. Protect adjacent wiring, insulation, and combustible construction whenever performing approved hot work. Reassemble all joints and perform a suitable leak check before charging or restarting.

Heat pump equipment can change operating mode without a local technician command. Defrost operation may temporarily change fan and refrigerant-system behavior. Auxiliary heat components, when equipped, can remain hot after a call ends. Allow components to cool before inspection. Keep hands, tools, and loose clothing away from fan paths. Avoid touching coil fins with unprotected hands.

### 1.5 Stop-work conditions

Do not proceed with startup if the roof curb is unstable, the unit has shipping damage affecting a pressure boundary, required clearance is obstructed, electrical data do not match the supply, the condensate drain is blocked, or the refrigerant detection system has been disabled. Record the condition, make the equipment safe, and obtain corrective direction. When a condition cannot be resolved using the rating plate, the figures in this manual, or the documented site design, contact Vantorr Technical Support with the model, rating-plate details, observations, and work already performed.

[[PAGEBREAK]]
## 2. Model number nomenclature

### 2.1 Reading the series and size designation

The VHP designation identifies a Vantorr packaged rooftop heat pump. The size suffix distinguishes the available nominal-capacity models. The listed capacity is a nominal model classification; actual delivered heating or cooling depends on operating conditions, installed airflow, duct resistance, and condition of the system. Use the corresponding specification and performance information rather than treating the model suffix as a measured field result.

| Model designation | Series meaning | Nominal capacity classification | Refrigeration system | Control board |
| --- | --- | --- | --- | --- |
| VHP-036 | Packaged rooftop heat pump | 3 tons | R-454B, single-stage scroll | VCB-210 |
| VHP-048 | Packaged rooftop heat pump | 4 tons | R-454B, single-stage scroll | VCB-210 |
| VHP-060 | Packaged rooftop heat pump | 5 tons | R-454B, single-stage scroll | VCB-210 |

### 2.2 Confirming the installed configuration

The model designation is only part of the equipment identification. The unit rating plate identifies the electrical configuration and equipment-specific data needed to select supply conductors, protective devices, and accessories. Confirm the complete model and available records before making changes to electrical or mechanical components. Do not infer voltage, phase, or factory-installed options from nominal tonnage alone.

> **NOTE:** A model designation describes the product family and size. It is not a substitute for the rating plate, electrical figure, or a field measurement.

[[PAGEBREAK]]
## 3. Specifications

### 3.1 VHP-036 specifications

| Field | Value |
| --- | --- |
| Nominal capacity (tons) | 3 |
| Refrigerant | R-454B |
| Cooling capacity (Btuh) | 35,300 |
| Factory refrigerant charge | 4 lb 0 oz |
| Minimum outdoor temperature for cooling | 35 °F |
| Anti-short-cycle delay | 5 minutes |
| Return air filters | 2 filters, 16 x 25 x 2 in. |
| Operating weight | 370 lb |
| Required clearances | service side 36 in., coil side 24 in., top 60 in. unobstructed |
| Voltage options | 208/230-1-60, 208/230-3-60 |
| Defrost interval | 30, 60 or 90 minutes (factory default 60 minutes) |

### 3.2 VHP-048 specifications

| Field | Value |
| --- | --- |
| Nominal capacity (tons) | 4 |
| Refrigerant | R-454B |
| Cooling capacity (Btuh) | 46,500 |
| Factory refrigerant charge | 5 lb 1 oz |
| Minimum outdoor temperature for cooling | 35 °F |
| Anti-short-cycle delay | 5 minutes |
| Return air filters | 2 filters, 20 x 25 x 2 in. |
| Operating weight | 480 lb |
| Required clearances | service side 36 in., coil side 24 in., top 60 in. unobstructed |
| Voltage options | 208/230-1-60, 208/230-3-60 |
| Defrost interval | 30, 60 or 90 minutes (factory default 60 minutes) |

### 3.3 VHP-060 specifications

| Field | Value |
| --- | --- |
| Nominal capacity (tons) | 5 |
| Refrigerant | R-454B |
| Cooling capacity (Btuh) | 59,300 |
| Factory refrigerant charge | 5 lb 15 oz |
| Minimum outdoor temperature for cooling | 35 °F |
| Anti-short-cycle delay | 5 minutes |
| Return air filters | 3 filters, 20 x 25 x 2 in. |
| Operating weight | 580 lb |
| Required clearances | service side 36 in., coil side 24 in., top 60 in. unobstructed |
| Voltage options | 208/230-3-60, 460-3-60 |
| Defrost interval | 30, 60 or 90 minutes (factory default 60 minutes) |

### 3.4 Applying specification data

The capacities in these tables describe factory-rated cooling performance, not a guaranteed field result under all conditions. The factory charge is a reference for an intact factory configuration. Do not add refrigerant solely because a field operating pressure appears different from an assumed value. Use the cooling charging chart for the exact model, verified operating conditions, and a suitable measurement procedure as described in Section 12.

> **CAUTION:** Do not extrapolate the charging, blower, electrical, or sensor data of one model to another. Select the figure for the unit being serviced and confirm that the measurement conditions match its axes and notes.

[[PAGEBREAK]]
## 4. Installation and clearances

### 4.1 Receiving and inspection

Inspect the shipment before removing packaging. Check the cabinet, coil guards, access panels, drain outlets, electrical enclosure, and visible tubing for damage or displacement. Compare the delivery information with the unit rating plate. Document transit damage before the unit is lifted or installed. Do not attempt to straighten damaged pressure tubing or place a visibly damaged refrigerant circuit in service.

### 4.2 Site assessment and support

Locate the equipment where outdoor airflow is unobstructed, conditioned-air ducts can be sealed, water can drain safely, and technicians can reach the service compartments. Review the roof structure and curb arrangement against the operating weight of the selected model. Verify the curb is properly supported and compatible with the unit base, duct openings, and weather seal. Provide roof flashing and waterproofing consistent with the building design.

> **WARNING:** Do not set a unit on an unverified roof curb or temporary support. A support failure can cause falling equipment, loss of roof integrity, and severe injury.

### 4.3 Rigging and setting the unit

1. Review the selected model's operating weight and the approved project lifting plan.
2. Inspect lifting equipment and confirm the cabinet can be handled without loading its panels or refrigerant piping.
3. Establish a controlled lift area and keep personnel away from the suspended unit and roof opening.
4. Lift and lower the unit in a controlled manner, maintaining its intended orientation.
5. Position the base on the prepared curb or approved mounting system without dragging it across the seal.
6. Confirm that the unit bears evenly on its support and that the weather seal remains continuous.
7. Inspect the cabinet, base, and service panels again for handling damage before proceeding.

Do not use ductwork or flashing to support the cabinet. If the curb profile or opening does not align, correct the mounting arrangement rather than forcing the cabinet into position. Recheck the site for objects left under the base before final securing.

### 4.4 Service and airflow clearances

Provide the clearances listed in Section 3 for the model installed: service side 36 in., coil side 24 in., top 60 in. unobstructed. Preserve these spaces after piping, electrical conduit, roof accessories, and nearby equipment are installed. Service clearance must permit removal of panels and safe access to the blower, electrical compartment, refrigerant service points, and coil surfaces. The top clearance is an airflow requirement and must not be filled with ductwork or overhead obstructions.

### 4.5 Supply and return duct connections

Use duct transitions that align with the unit openings without distorting the base. Support duct weight independently and provide flexible connections where required by the project design. Seal seams and penetrations so that rainwater, unconditioned air, and construction debris cannot enter the system. Insulate ducts according to the design conditions to prevent unwanted heat gain, heat loss, or condensation.

### 4.6 Final placement review

Before making utility connections, confirm that the unit is stable, service access is available, the outdoor air path is clear, the supply and return connections are sealed, and the roof penetration is weather-tight. Record any site limitation that could affect maintenance. Complete leveling and condensate work under Section 5 before allowing the system to cool or defrost. Check that all transport-related material has been removed from the airflow path.

> **NOTE:** Installation drawings establish the intended duct routing and support arrangement. This manual establishes equipment handling and operating requirements; neither document replaces a field inspection of the completed installation.

[[PAGEBREAK]]
## 5. Leveling and condensate

### 5.1 Cabinet level and drainage direction

The unit must be level within 1/4 in. side to side so the condensate and defrost water drain correctly.

Check the unit on the installed curb rather than on the roof surface. Use a suitable level on sound reference surfaces and check the cabinet in the required directions. Correct an uneven support with approved curb or support adjustments; do not distort the unit base by pulling it down against a gap. Reinspect the roof seal after any correction. Drainage depends on the internal pan geometry remaining in its intended orientation.

> **CAUTION:** An out-of-level cabinet can retain water, overflow the drain pan, wet insulation, or permit ice accumulation. Do not try to compensate by drilling additional drain holes in the unit.

### 5.2 Condensate connection and trap

Identify the factory condensate outlet before piping. Install a suitable drain connection using materials compatible with the expected water conditions and local requirements. Arrange a trap when required by the drain-pan pressure relationship and the site design. A trap must be configured for the actual installed application; a drawing of a generic trap does not establish its required dimensions.

Run the drain with continuous fall to an approved disposal point, secure it independently of the cabinet, and provide access for inspection and cleaning. Avoid routing that may freeze, siphon, or discharge onto walkways, roof membranes, electrical equipment, or building entrances. Do not connect the condensate drain to a closed system that can impose pressure on the unit pan unless an engineered separation is provided.

1. Confirm that the cabinet is level and the drain outlet is free of packing material.
2. Inspect the pan for debris, construction dust, and signs of transit damage.
3. Assemble and support the drain without applying bending force to the outlet.
4. Verify the trap arrangement and discharge location against the site design.
5. Introduce water into the pan through an accessible approved location and observe the flow.
6. Check all joints and the roof penetration for leakage, standing water, or backflow.
7. Restore access panels and record the test result before starting cooling operation.

### 5.3 Defrost water management

Heat pump operation produces water at the outdoor coil during defrost. Provide a clear, safe runoff route and consider how the roof will handle water during freezing weather. Do not block factory drainage paths with roofing compound, insulation, or equipment stands. Inspect areas where defrost water could collect beneath the unit or refreeze on a service path. Correct drainage problems before they lead to accumulated ice around the cabinet or nearby equipment.

### 5.4 Drain service checks

Inspect the pan and drain during seasonal service and whenever water is reported around the unit. Remove obstructions using methods that will not damage the pan or force debris back into the air section. If water persists after cleaning, check level, trap condition, outlet alignment, drain routing, and the possibility of condensation on uninsulated duct surfaces. Do not apply sealant over a drain opening to stop an unexplained leak.

> **NOTE:** Record whether water appears during cooling, heating defrost, or when the unit is off. The operating context helps distinguish a blocked indoor drain from normal outdoor defrost runoff or a roof penetration leak.

[[PAGEBREAK]]
## 6. Electrical connections

### 6.1 Electrical data and reference drawing

The VHP Series Control Wiring Diagram and Electrical Data figure identifies the factory wiring arrangement and electrical data for the available configurations. Read the figure by first locating the installed model and supply configuration, then following its labeled circuits and data fields; use the unit rating plate to confirm the selection and never transfer values from another configuration.

[[FIGURE:VHP-WD]]

> **WARNING:** Improper wiring, unsuitable overcurrent protection, or incorrect supply voltage can cause electric shock, fire, and equipment damage. Electrical work must comply with the actual rating plate, the figure above, and applicable electrical requirements. Do not select a protective device by nominal tonnage.

### 6.2 Supply power, disconnect, and grounding

Provide a suitable supply and disconnect arrangement for the installed voltage and phase shown on the rating plate. Confirm that the source is consistent with the ordered equipment before terminating conductors. Locate the disconnect so the equipment can be safely isolated for service in accordance with applicable requirements. Protect conductors from sharp edges, vibration, water entry, and heat exposure. Use listed fittings and approved entry points; do not create openings that compromise the refrigerant detection system or weather protection.

Size conductors and overcurrent protection from the rating plate and the VHP Series Control Wiring Diagram and Electrical Data figure. Check circuit identification at the power source and the equipment. Bond and ground the cabinet as required by the approved installation. Verify continuity of protective grounding before startup. Do not use a refrigerant tube, condensate pipe, roof deck, or duct as the grounding path.

### 6.3 Field wiring practice

1. Isolate and lock out supply power, then verify that the intended circuit is de-energized.
2. Compare the nameplate electrical configuration with the site supply and approved drawings.
3. Inspect the electrical enclosure for moisture, damage, loose parts, and shipping debris.
4. Route power and control conductors through appropriate protected entries.
5. Make connections only as identified in the VHP Series Control Wiring Diagram and Electrical Data figure.
6. Tighten connections using the requirements for the installed connection hardware and inspect for stray strands.
7. Secure wiring away from moving parts, coil edges, hot surfaces, and service-panel paths.
8. Check grounding, enclosure seals, strain relief, and access before applying power.

### 6.4 Pre-energization and verification

Before energizing, confirm that the supply is correct, wiring is mechanically secure, the blower turns freely with power removed, panels are installed as required, and the air path is open. Verify the refrigerant detection system remains connected and undamaged. Energize the unit under controlled startup conditions, observe the VCB-210 status indication, and check for abnormal noise, odor, heating, or protective interruption. If anything appears unsafe, isolate power and investigate rather than repeatedly cycling the disconnect.

The control circuit and compressor protection features are not replacements for a proper supply. A control indication cannot validate phase, grounding, conductor selection, or circuit protection. Use direct measurements and the equipment-specific documentation for those checks.

> **CAUTION:** Never use an oversized protective device to prevent nuisance interruptions. Determine the cause of the interruption and correct the fault using the unit rating plate and applicable electrical requirements.

[[PAGEBREAK]]
## 7. Thermostat and controls

### 7.1 VCB-210 control overview

The VCB-210 coordinates the heat pump's normal cooling, heating, defrost, and protective functions. It receives calls from the field thermostat, processes the conditions required for equipment operation, and commands the applicable equipment outputs. It also provides status information for diagnostics. Do not treat a thermostat call as proof that a compressor or fan must start immediately; the control may be observing a protective delay or responding to another operating condition.

Select a thermostat suitable for a heat pump with auxiliary electric heat when that accessory is installed. Verify compatibility and configuration using the installed thermostat's instructions and the VHP Series Control Wiring Diagram and Electrical Data figure. A conventional cooling-only thermostat may not provide the functions required for heat pump operation. Do not determine reversing-valve control logic by comparing VHP wiring to a different product series.

> **CAUTION:** Incompatible thermostat logic can produce incorrect mode operation or unwanted auxiliary heat. Confirm the actual control application rather than assuming that a setting used at another site applies to this installation.

### 7.2 Control wiring and thermostat location

Route thermostat cable away from high-voltage conductors and known sources of interference, using separate pathways where required. Protect exposed cable and entry points against abrasion and moisture. Make control connections only according to the electrical figure and the instructions supplied with compatible field devices. Maintain identification of the cable at the thermostat and equipment; undocumented splices complicate diagnosis of intermittent operation.

Install the thermostat where it measures representative occupied-space temperature, away from direct sun, supply-air discharge, unconditioned exterior surfaces, and localized heat sources. Confirm that the thermostat has stable power, a readable display, and an accurate mode selection. A poorly located thermostat may cause short run cycles or comfort complaints even when the rooftop equipment is working correctly.

### 7.3 Normal operating commands

The thermostat requests cooling or heating based on space conditions and its selected mode. The VCB-210 accepts the request when the required conditions are met, starts the applicable equipment, and monitors operation. When the call is satisfied, the control ends the active demand and returns the equipment to its normal standby condition. Some components may not stop at precisely the same instant as the call; assess operation against the current mode and documented control behavior rather than assuming a fault from an isolated sound.

### 7.4 Setup and functional checks

1. Verify the thermostat type and approved application for a heat pump.
2. Confirm the required thermostat functions are configured under the thermostat manufacturer's instructions.
3. Inspect the control wiring route and compare its connections with the VHP electrical figure.
4. Restore power and confirm that the VCB-210 shows an interpretable operating status.
5. Request cooling and observe whether the unit responds in the sequence described in Section 8.
6. Remove the cooling call, then request heating and observe Section 9.
7. Verify auxiliary heat only if a compatible installed kit is present and a safe test condition exists.
8. Return the thermostat to the owner's intended schedule and record the results.

If the equipment does not respond to a valid call, check the state of protective devices, control power, the status indication, and the integrity of the wiring. Do not replace the control board solely because a thermostat call did not start the compressor. Section 17 provides a systematic troubleshooting order.

> **NOTE:** Record the thermostat's displayed mode and requested function before clearing a complaint. A later technician needs to know whether the problem occurred in heating, cooling, defrost, or auxiliary heat operation.

[[PAGEBREAK]]
## 8. Sequence of operation — cooling

### 8.1 Conditions for cooling

A cooling request begins at a compatible thermostat and is interpreted by the VCB-210. Before starting the compressor, the control must permit operation under the current protective conditions. The minimum outdoor temperature for cooling is 35 °F for each listed VHP model. Operation outside the documented range must not be assumed acceptable simply because the thermostat can request cooling.

The anti-short-cycle delay is 5 minutes. This delay helps prevent immediate compressor restart after an operating interruption. If a call is made while the delay is active, allow the control to complete its normal timing. A brief absence of compressor operation immediately after a new call does not, by itself, establish a failed contactor or compressor.

### 8.2 Cooling startup and operation

1. The thermostat recognizes a need for cooling and sends the appropriate request to the VCB-210.
2. The board evaluates the requested mode and applicable safety and timing conditions.
3. When operation is permitted, the refrigerant circuit begins cooling operation and the indoor air system delivers air across the indoor coil.
4. Outdoor airflow removes heat from the refrigeration system through the outdoor coil section.
5. Moisture condensed from return air collects in the indoor drain pan and leaves through the installed condensate drain.
6. The control continues to supervise the equipment until the cooling request ends or a protective condition requires a change.

The refrigeration circuit includes components that direct refrigerant flow for the requested operating mode. Their field diagnosis must follow the equipment wiring and operating evidence; do not infer control logic or refrigerant flow from a generic heat pump diagram. Maintain free airflow at both coils throughout operation.

### 8.3 Cooling shutdown and restart

If a protection interrupts cooling, inspect the board's status indication and the underlying operating conditions before resetting or cycling power. Common contributors include airflow restriction, blocked outdoor coil surfaces, electrical supply problems, and refrigerant-system faults. A correct repair addresses the root cause rather than masking the protective response.

### 8.4 Cooling performance verification

After startup stabilizes, check supply and return air conditions, indoor airflow, condensate disposal, outdoor coil airflow, and the overall sound and vibration of the unit. Compare measured electrical and refrigeration conditions only with the applicable rating plate and model-specific figures. Changes in load can affect observations; record outdoor and indoor conditions alongside measurements so later comparisons are meaningful.

> **NOTE:** Diagnose poor cooling in a defined order: confirm the thermostat request, check control status, establish airflow, inspect coil condition, and then evaluate the refrigerant system with the correct charging chart. Do not use refrigerant addition as a general correction for weak cooling.

[[PAGEBREAK]]
## 9. Sequence of operation — heating and auxiliary heat

### 9.1 Heat pump heating

In heating mode, the thermostat requests space heat and the VCB-210 operates the heat pump when the necessary conditions are satisfied. The refrigeration system transfers heat from the outdoor environment into the indoor air stream. The indoor blower moves return air across the conditioned-air coil and through the supply duct system. Outdoor coil temperature and outdoor humidity affect frost formation and may lead to defrost operation under Section 10.

1. The thermostat determines that space heat is required and sends a heat pump heating request.
2. The VCB-210 evaluates the request along with operating and protective conditions.
3. When allowed, the compressor and associated airflow equipment operate to deliver heat to the occupied space.
4. The control monitors operation while the thermostat continues to call for heat.
5. A defrost requirement may temporarily change the operating sequence while protecting indoor comfort and the outdoor coil.
6. When the thermostat is satisfied, heating demand ends and the equipment returns to standby under normal control supervision.

Do not judge heating performance by supply-air temperature alone. Heat pump delivery changes with outdoor conditions and indoor airflow. Examine the space load, thermostat demand, blower delivery, outdoor-coil condition, and any auxiliary heat operation together.

### 9.2 Auxiliary electric heat

Auxiliary electric heat kits are available in 5, 10 and 15 kW sizes.

An auxiliary heat kit is an accessory, not an assumed standard component of every VHP unit. Confirm installation and compatibility from the unit records, physical inspection, electrical figure, and accessory instructions before testing. An approved thermostat and control arrangement must request auxiliary heating only under the conditions for which the installed system was designed.

> **WARNING:** ELECTRIC HEAT HAZARD. An installed auxiliary heat assembly contains components that can become extremely hot and presents an electrical hazard. Lock out all applicable supply sources and allow the assembly to cool before touching or inspecting it. Never operate the assembly without the required airflow and safety devices.

### 9.3 Heating with defrost demand

Observe the full operating context before declaring an abnormal defrost condition. A unit that briefly changes behavior and then resumes heating may be following the intended control sequence. Persistent heavy ice, repeated interruptions, or failure to return to heating requires further inspection of the coil, sensor, drainage, and status indication.

### 9.4 Heating shutdown and safety response

When the space temperature requirement is met, the thermostat ends the heating request. The VCB-210 returns the system to a nonheating condition while enforcing protective logic. Do not isolate power merely to end a normal call; use the thermostat for ordinary operation and the electrical disconnect for service. Where overheating, electrical odor, arcing, or abnormal noise is suspected, remove the unit from service safely and investigate before another start attempt.

> **NOTE:** When diagnosing an apparent lack of heat, identify whether the compressor, indoor blower, auxiliary heat, or defrost sequence is involved. The corrective action for a missing thermostat request differs from the action for a refrigeration-system problem.

[[PAGEBREAK]]
## 10. Defrost operation

### 10.1 Purpose and normal conditions

The outdoor coil can collect frost when the heat pump extracts heat from outdoor air. Frost restricts airflow and reduces heat transfer, so the VCB-210 provides a defrost function. The control uses an operating interval and outdoor-coil sensing to determine when defrost is appropriate. Interval selection alone does not establish that the coil needs defrost, and elapsed heating time alone is not proof that the coil is iced.

Defrost interval options are 30, 60 or 90 minutes (factory default 60 minutes). These are the available interval selections for the listed VHP models. Leave the factory selection in place unless a documented commissioning requirement calls for a change using approved service information. Do not invent a setting method from the visible board hardware or borrow a procedure from a different control board.

### 10.2 Defrost sequence

During eligible heating operation, the VCB-210 supervises the defrost timing and the outdoor-coil temperature information. When the required conditions are present, the unit enters a defrost operating state intended to clear frost from the outdoor coil. The equipment may temporarily alter outdoor airflow and refrigerant-system operation. Water released from melting frost must be able to drain away from the outdoor section.

When defrost is complete, the control returns the system to normal heating operation as permitted by the thermostat demand and protective conditions. The indoor comfort response depends on the installed control arrangement and any compatible auxiliary heat. The service technician should assess whether frost is removed, drainage is clear, and heating resumes rather than judging the process solely by fan noise.

> **CAUTION:** Never scrape the outdoor coil with a sharp tool or apply concentrated heat to remove frost. Damage to coil tubing or fins can lead to poor performance or refrigerant loss. Address the underlying defrost or drainage problem instead.

### 10.3 Checking a suspected defrost problem

1. Confirm the thermostat is requesting heating and that the unit has been operating under conditions where frost can form.
2. Inspect the outdoor coil for the distribution of frost and for physical obstruction by leaves, debris, or snow.
3. Check that outdoor airflow is not blocked and that the fan area is free of ice buildup.
4. Inspect the outdoor-coil sensor attachment and its visible wiring with the equipment made safe.
5. Evaluate the sensor using the method in Section 11 and the VHP Series Sensor Resistance vs. Temperature figure.
6. Read the VCB-210 status indication using the VHP Series Status LED Flash Codes figure.
7. Observe a complete eligible operating sequence when safe, recording frost removal, water drainage, and return to heating.

### 10.4 Documentation

Record outdoor conditions, thermostat demand, visible coil frost, selected interval if confirmed from approved instructions, sensor evaluation, and observed control status. If defrost does not complete properly and the cause remains unclear, leave the equipment in a safe condition and contact Vantorr Technical Support. Describe the observations without interpreting an unknown status indicator from memory.

[[PAGEBREAK]]
## 11. Defrost / outdoor coil sensor check

### 11.1 Sensor function and inspection

The outdoor-coil sensor provides temperature information used in defrost supervision. A loose, displaced, damaged, or electrically open sensor circuit can produce misleading information even when the refrigeration system is mechanically sound. Inspect the sensor's physical condition and placement before assuming that the sensing element has failed. Confirm that its lead is protected from moving parts, cabinet edges, and water damage.

> **WARNING:** Disconnect and lock out power before disconnecting a sensor or measuring resistance in its circuit. Resistance measurements made on an energized circuit may injure the technician or damage the instrument and control board.

### 11.2 Using the resistance curve

The VHP Series Sensor Resistance vs. Temperature figure provides the reference relationship for checking the outdoor-coil sensor. Read it by finding the measured sensor temperature on the temperature axis, then tracing to the curve and across to the resistance axis; compare that plotted resistance with the isolated sensor measurement without extrapolating beyond the figure.

[[FIGURE:VHP-TH]]

### 11.3 Field check procedure

1. Note the operating complaint, outdoor conditions, and any VCB-210 status indication.
2. Isolate and verify electrical power before opening the relevant access area.
3. Examine the sensor body, mounting contact, lead routing, and connection for looseness or damage.
4. Disconnect the sensor from control circuitry as required for an independent measurement.
5. Measure the sensor temperature at the location being evaluated.
6. Measure sensor resistance with a suitable instrument and compare it with the VHP Series Sensor Resistance vs. Temperature figure.
7. Inspect the sensor lead and connection for intermittent continuity or contamination when the result does not agree with the figure.
8. Reconnect the sensor, secure the wiring, reinstall panels, and retest operation under safe conditions.

Do not test a sensor by shorting its connections to the board or applying an external voltage. Such methods can damage controls or create an unsafe operating condition. If the measured value disagrees with the curve, verify meter setup, temperature measurement, connection state, and sensor contact before making a replacement decision.

### 11.4 Interpreting results

An apparently correct resistance reading does not guarantee correct operation if the sensor is poorly attached to the coil or its wiring is intermittent. Conversely, an out-of-range reading may reflect a measurement made at the wrong temperature or through connected circuitry. Confirm both the electrical relationship and the physical installation. If the sensor evaluates correctly but defrost remains abnormal, inspect outdoor airflow, coil condition, drainage, and VCB-210 status before replacing the board.

> **NOTE:** Use the curve for the installed VHP equipment. Do not substitute a generic sensor table, a different series' curve, or a resistance value recalled from earlier service work.

[[PAGEBREAK]]
## 12. Refrigerant charging in cooling mode

### 12.1 General charging requirements

Charging evaluation must be performed in cooling mode under stable conditions using the charging chart for the exact model. These VHP units use R-454B; all instruments, recovery equipment, charging equipment, and refrigerant containers must be suitable for that refrigerant and A2L service. Follow approved handling procedures and use appropriate ventilation. Never use another refrigerant to correct a performance concern.

The factory charge shown in Section 3 describes the factory configuration. It is not an instruction to add that quantity to a running system or an allowance for an unknown leak. On an intact factory circuit, begin with the delivered charge and investigate airflow, coil cleanliness, operating conditions, and measurement technique before changing refrigerant mass. After a circuit has been opened or a charge has been recovered, follow a documented repair, evacuation, leak test, and weighing process consistent with approved R-454B practice.

> **WARNING:** Refrigerant release and ignition sources can create an A2L hazard. Do not vent refrigerant or attempt charging in an unsafe area. Keep ignition sources controlled and use only refrigerant-service equipment approved for this application.

### 12.2 VHP-036 cooling charge evaluation

The VHP-036 Cooling Charging Chart is the charging reference for model VHP-036. Read the chart by selecting the applicable operating condition on its axes, locating the corresponding chart relationship, and comparing the indicated target with measured system conditions; use only values displayed in that chart.

[[FIGURE:VHP-036-CC]]

1. Verify the VHP-036 rating plate and the required cooling operating conditions.
2. Check both coil air paths, return filters, and the condensate system.
3. Connect approved R-454B service instruments using safe procedures.
4. Operate the system in cooling and document the conditions needed to read the chart.
5. Locate the indicated reference on the VHP-036 Cooling Charging Chart and compare it with measured conditions.
6. If the comparison is abnormal, investigate airflow and refrigeration faults before making a charge correction.
7. When work is complete, secure service connections, check for leaks, and restore the cabinet.

### 12.3 VHP-048 cooling charge evaluation

The VHP-048 Cooling Charging Chart is the charging reference for model VHP-048. Read the chart by matching its operating-condition axes to field measurements, tracing to the applicable plotted relationship, and reading the corresponding target from the figure; do not use the VHP-036 or VHP-060 chart.

[[FIGURE:VHP-048-CC]]

1. Confirm model identity, refrigerant, supply configuration, and the current cooling request.
2. Inspect filters, coil cleanliness, duct openings, outdoor airflow, and drain operation.
3. Install suitable instruments without creating an avoidable refrigerant release.
4. Record operating conditions and locate the matching point on the VHP-048 Cooling Charging Chart.
5. Compare the chart reference with the observed system conditions.
6. Address a confirmed refrigerant-side issue using approved recovery and charging methods, not arbitrary additions.
7. Recheck operating behavior, service-port integrity, and leak tightness before leaving the unit.

### 12.4 VHP-060 cooling charge evaluation

The VHP-060 Cooling Charging Chart is the charging reference for model VHP-060. Read it by finding the applicable field conditions on the labeled chart axes, following the indicated curve or relationship, and comparing the resulting reference with the measured refrigeration condition without estimating an unshown target.

[[FIGURE:VHP-060-CC]]

1. Verify the rating plate identifies model VHP-060 and refrigerant R-454B.
2. Confirm that the cooling request is valid and operation is stable.
3. Inspect filter loading, indoor blower performance, outdoor coil condition, and unobstructed discharge.
4. Connect approved instruments and record the operating conditions shown on the chart axes.
5. Read the VHP-060 Cooling Charging Chart and compare the chart reference with actual measurements.
6. Determine the cause of any discrepancy before adjusting charge.
7. Finish with a leak check, correctly secured service connections, and restored access panels.

### 12.5 Interpreting a charging discrepancy

A pressure or temperature observation can be affected by the load, metering-device operation, noncondensables, coil condition, airflow restriction, sensor placement, and instrument error. The charging chart is a diagnostic reference only when its stated conditions are met. Do not adjust charge based on a single reading without confirming system stability and the other supporting evidence.

> **NOTE:** The chart establishes model-specific charging targets. This text intentionally does not provide a substitute pressure, temperature difference, superheat, or subcooling target. Read the indicated values directly from the correct figure during service.

[[PAGEBREAK]]
## 13. Indoor airflow adjustment

### 13.1 General airflow requirements

Indoor airflow affects cooling capacity, heating delivery, coil temperature, condensate removal, and auxiliary heat operation. Establish correct airflow before using refrigerant measurements to diagnose charge. The installed duct system, filter condition, coil cleanliness, and blower configuration must be considered together. A clean unit with an undersized or restricted duct system may still fail to deliver the intended air volume.

Measure external static pressure with appropriate instruments at valid locations in the installed system. Refer to the blower figure for the exact model to relate the measured condition to available blower performance. Do not use a remembered airflow value or borrow a fan table from another size. If the measured operating point is outside the documented figure, correct the installation condition or obtain engineering direction rather than projecting a result beyond the plotted range.

> **CAUTION:** Do not operate the blower against blocked ducts or with filters removed as a routine adjustment method. A change that appears to increase airflow may also reduce filtration effectiveness or expose the coil and blower to debris.

### 13.2 VHP-036 indoor blower performance

The VHP-036 Indoor Blower Performance figure shows the available blower relationships for the VHP-036. Read it by locating the measured system static pressure and the applicable blower operating selection on the figure, then reading the corresponding airflow from its labeled intersection.

[[FIGURE:VHP-036-BT]]

| VHP-036 adjustment check | Field action | Reference |
| --- | --- | --- |
| Installed return filters | Confirm correct fit and cleanliness | Section 3.1 |
| Duct system resistance | Measure external static pressure | VHP-036 blower figure |
| Blower performance | Compare the selected operating point | VHP-036 blower figure |
| Final condition | Record airflow interpretation and system response | Commissioning record |

Adjust the blower only through approved service methods for the installed assembly. After an adjustment, repeat the static pressure check and inspect operation in both cooling and heating. Verify that the return grille and duct path remain unobstructed.

### 13.3 VHP-048 indoor blower performance

The VHP-048 Indoor Blower Performance figure provides the model-specific blower data. Read the figure by selecting the measured static-pressure condition and applicable blower selection, then tracing to the airflow scale; do not transfer a VHP-036 result to this model.

[[FIGURE:VHP-048-BT]]

| VHP-048 adjustment check | Field action | Reference |
| --- | --- | --- |
| Installed return filters | Confirm correct fit and cleanliness | Section 3.2 |
| Duct system resistance | Measure external static pressure | VHP-048 blower figure |
| Blower performance | Compare the selected operating point | VHP-048 blower figure |
| Final condition | Record airflow interpretation and system response | Commissioning record |

If delivered airflow is inadequate, inspect filter loading, coil fouling, duct restrictions, closed dampers, and blower condition before changing the operating selection. Keep the measurement method consistent when comparing before-and-after results.

### 13.4 VHP-060 indoor blower performance

The VHP-060 Indoor Blower Performance figure gives the performance relationship for this model. Read it by identifying the measured duct static pressure and the applicable blower condition, then following the displayed relationship to its airflow indication without extrapolating outside the figure.

[[FIGURE:VHP-060-BT]]

| VHP-060 adjustment check | Field action | Reference |
| --- | --- | --- |
| Installed return filters | Confirm correct fit and cleanliness | Section 3.3 |
| Duct system resistance | Measure external static pressure | VHP-060 blower figure |
| Blower performance | Compare the selected operating point | VHP-060 blower figure |
| Final condition | Record airflow interpretation and system response | Commissioning record |

The VHP-060 uses the return filter arrangement listed in Section 3.3. Confirm that all filter positions are filled with the correct size and that the filter rack seals against bypass. Recheck static pressure after replacing loaded filters.

### 13.5 Final airflow verification

Document the measured system condition, the figure used, the selected blower operating condition, and the observed temperature and noise response. Inspect for vibration, cabinet air leakage, condensate carryover, and unusual duct noise. Perform another airflow check whenever ductwork, filters, or blower components are substantially changed. An airflow adjustment is complete only when the installed system operates safely in its intended modes.

[[PAGEBREAK]]
## 14. Refrigerant detection system (A2L)

### 14.1 System purpose

The VHP Series includes a refrigerant detection system intended to support the unit's A2L refrigerant safety functions. The system monitors for a refrigerant-related condition and participates in the equipment's protective response. Maintain the factory sensor, wiring, associated control functions, and intended air paths in the condition required by the equipment design. Do not defeat detection or mitigation features to maintain temporary comfort.

> **WARNING:** A disabled, disconnected, or bypassed refrigerant detection system can leave an R-454B release without the intended equipment protective response. Remove equipment with a suspected detection-system fault from normal service until it has been assessed and made safe.

### 14.2 Installation and inspection

Inspect detection-system components during equipment receiving and before startup. Look for physical damage, detached wiring, obstructed sensing locations, corrosion, contamination, or unauthorized modifications. Do not relocate the sensor, cover an opening, alter the air path, or move wiring based on an assumption about better detection. Preserve factory protection against water and debris. Follow approved equipment instructions when replacing an affected component.

### 14.3 Response to a detection condition

When a refrigerant-related condition is indicated, treat it as a potential leak until investigated by qualified personnel using approved A2L procedures. Follow the site's safety plan, control possible ignition sources, and use suitable independent leak-detection equipment. Do not assume the system is safe simply because a thermostat demand is removed or the status indication changes. The protective response must be resolved before normal operation resumes.

1. Stop work that could introduce an ignition source and assess the area safely.
2. Follow the facility's applicable ventilation, access-control, and emergency procedures.
3. Observe and document available equipment indications without defeating any protective function.
4. Investigate the suspected release with approved tools and methods.
5. Repair and verify any confirmed leak under the proper refrigerant-handling procedure.
6. Inspect the detection system and restore the unit only when safe operation is verified.

### 14.4 Service limits

Do not create a refrigerant release to demonstrate a sensor response. Do not force control outputs or substitute arbitrary electrical signals for a sensor without a documented, approved test method. If the system indicates a fault or an unexplained mitigation condition, use the VCB-210 status information and contact Vantorr Technical Support as necessary. Record the observed conditions and work performed, without assuming that a cleared indication proves the source of the problem was repaired.

[[PAGEBREAK]]
## 15. Control board diagnostics

### 15.1 Reading the VCB-210 status indication

The VCB-210 provides a status LED to assist with operating and fault diagnosis. The VHP Series Status LED Flash Codes figure identifies the displayed patterns and their meanings. Read the figure by observing the complete LED indication, locating the matching pattern in the figure, and following its listed diagnostic guidance; do not interpret the indication by memory or from another product series.

[[FIGURE:VHP-LED]]

> **WARNING:** Diagnostic observation may expose energized components. Only qualified personnel may perform live electrical testing, using appropriate protective measures. Make the equipment electrically safe before touching wiring, board connections, or moving equipment.

### 15.2 Diagnostic procedure

1. Confirm the unit model, current thermostat request, and operating mode.
2. Determine whether there is an active protective condition or an ordinary control delay.
3. Observe the VCB-210 indication without touching energized parts.
4. Match the indication to the VHP Series Status LED Flash Codes figure.
5. Inspect the related system condition using approved, safe measurement methods.
6. Correct the verified cause and restore all protective devices and connections.
7. Observe normal operation and record the final status.

### 15.3 When the indication is unclear

If the LED cannot be observed, first establish whether proper power reaches the equipment using safe methods and the electrical figure. Inspect for water damage, loose connections, or an interrupted protective circuit. Do not create unauthorized bridges to make the indicator operate. If the observed pattern does not clearly match the figure, record it and request guidance from Vantorr Technical Support. Avoid speculative replacement of the VCB-210.

> **NOTE:** The same comfort complaint can result from a thermostat problem, an active protective response, or a mechanical failure. Record the actual LED observation and the conditions when it occurred.

[[PAGEBREAK]]
## 16. Maintenance schedule

### 16.1 Routine maintenance program

Maintain the VHP as part of the facility's preventive maintenance program. The schedule below provides inspection events, not substitute performance limits. Adjust inspection frequency for site dust, operating hours, weather exposure, and observed conditions. Service must be performed safely with access and isolation appropriate to the work. Correct safety-related defects before the equipment is returned to service.

| Maintenance event | Items to inspect | Required action | Record |
| --- | --- | --- | --- |
| Regular operator inspection | Thermostat operation, unusual sound, visible water | Report abnormal behavior; keep air openings clear | Date and observation |
| Filter service | Filter loading, fit, rack seals | Clean or replace with listed model size as applicable | Filter condition |
| Cooling-season inspection | Indoor coil, drain pan, trap, outdoor coil | Clean safely; verify condensate flow and coil airflow | Drain and coil condition |
| Heating-season inspection | Outdoor coil, defrost drainage, sensor attachment | Clear obstructions; verify heating and defrost behavior | Operating observations |
| Electrical service | Enclosure, grounding, field connections, wire protection | Inspect with power isolated; correct damage | Findings and corrections |
| Refrigeration service | Tubing condition, signs of leakage, service-port integrity | Investigate suspected leaks using approved A2L methods | Leak-check outcome |
| Control and detection check | VCB-210 status, refrigerant detection components | Verify condition without bypassing protection | Status and inspection |
| Periodic performance review | Duct resistance, blower performance, operating symptoms | Compare with correct model figures | Measurements and figure |

### 16.2 Filter and coil care

Use the model-specific return filter sizes in Section 3. Keep the complete filter bank installed and correctly seated. Inspect filters sooner when construction, renovation, or unusual dust is present. A heavily loaded filter can affect both heating and cooling and can make refrigerant readings misleading. Inspect coil surfaces for dust, lint, and damage. Clean with methods suitable for the materials and the site; protect electrical components and refrigerant detection hardware from wash water.

### 16.3 Drainage, electrical, and control checks

Confirm the indoor condensate pan and drain flow freely. Check outdoor defrost runoff paths before freezing weather. Inspect the cabinet for corrosion, loose panels, damaged seals, and water entry. With equipment safely isolated, look for overheated electrical connections, worn insulation, loose supports, and moisture. Recheck the VCB-210 status after service using Section 15. Verify all panels and protective covers are restored.

### 16.4 Maintenance records

Keep a record of service date, model, observed operating mode, thermostat demand, filter condition, cleaning performed, measured system conditions, figures consulted, repairs made, and final status. When a refrigerant repair is performed, document the handling and leak verification required by applicable practice. Make records available to the owner and future technicians. Trend recurring findings rather than treating each visit as an isolated event.

[[PAGEBREAK]]
## 17. Troubleshooting

### 17.1 General approach

Begin by confirming the reported symptom, thermostat setting, operating mode, and present control status. Check basic airflow and power conditions before pursuing complex refrigerant faults. A symptom should be reproduced only when doing so is safe. Use the VHP Series Status LED Flash Codes figure for board indications, the VHP Series Control Wiring Diagram and Electrical Data figure for electrical verification, and the appropriate model chart for refrigeration or blower evaluation.

> **WARNING:** Stop troubleshooting if electrical arcing, an apparent refrigerant leak, disabled A2L protection, structural instability, or a dangerous access condition is present. Make the installation safe and follow the applicable hazard procedure before additional testing.

| Symptom | Initial checks | Likely area to investigate | Next action |
| --- | --- | --- | --- |
| Unit does not respond | Thermostat request, disconnect, control status | Field power or control circuit | Compare with electrical figure; verify safely |
| Compressor does not start after call | Active demand, protective timing, board indication | Normal delay or protective interruption | Allow delay; use LED figure if unresolved |
| Indoor blower absent | Filter and duct area, control request, board status | Blower power or control | Inspect with power isolated; use wiring figure |
| Weak cooling | Filters, indoor airflow, outdoor coil, stable operating conditions | Airflow or refrigeration system | Use blower and cooling charging figures |
| Weak heating | Thermostat demand, airflow, outdoor coil | Heat transfer or mode control | Verify heating sequence and status |
| Auxiliary heat unavailable | Accessory presence, thermostat demand, airflow | Accessory or control connection | Use approved accessory and electrical information |
| Outdoor coil heavily iced | Coil obstruction, drainage, sensor contact | Defrost sensing or operation | Follow Sections 10 and 11 |
| Water at indoor section | Cabinet level, pan, trap, drain line | Condensate drainage | Clear restriction and retest drainage |
| Ice or water around outdoor base | Drain path, weather conditions, outdoor section | Defrost runoff obstruction | Restore safe drainage route |
| Repeated protective interruption | Board status, supply, coils, airflow | Safety or operating condition | Identify cause before restart |
| Suspected refrigerant leak | Odor or instrument indication, protected-area condition | Refrigerant circuit | Apply A2L leak procedure and repair |
| Refrigerant detection indication | Detection system, relevant board status | A2L protective response | Keep equipment safe; follow Section 14 |
| Unusual fan noise or vibration | Cabinet fasteners, debris, airflow path | Fan or mechanical assembly | Isolate power and inspect |
| Erratic temperature control | Thermostat location, wiring, operating requests | Thermostat or control communication | Compare with Section 7 and wiring figure |
| Charging comparison appears abnormal | Operating stability, airflow, instruments | Measurement or refrigeration condition | Recheck correct model chart |

### 17.2 Returning the equipment to service

Following a repair, verify the corrected condition, required airflow, condensate and defrost drainage, control operation, and condition of the A2L detection system. Restore all electrical enclosures and service panels. Observe the unit in the mode related to the original complaint and confirm that no unexplained status indication remains. Record the final measurements and identify the figures used to interpret them.

If the cause is not established, do not replace several unrelated parts as a trial. Secure the equipment, preserve relevant observations, and contact Vantorr Technical Support with the model, rating-plate configuration, symptom history, control indication, measurements, and corrective steps already completed.
