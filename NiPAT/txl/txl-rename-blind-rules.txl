include "txl.grm"
include "bom.grm"

%Redefine in ruleStatement
redefine functionStatement
[empty]
end redefine

%ReDefinition to include rule, function, replace, match

redefine ruleStatement
	[ruleHeader] [NL] [IN]
	[ruleBody]
	[ruleFooter]
end redefine


define ruleHeader
		'rule [ruleid] [repeat formalArgument]	
	| 	'function [ruleid] [repeat formalArgument]
end define

define ruleBody
		[repeat constructDeconstructImportExportOrCondition] 	
		[EX] [opt skippingType]
		[replace_match] [EX] 
end define

define replace_match
	'replace [opt dollarStar] [SP] [type]			[NL][IN] 
			[pattern]
		[repeat constructDeconstructImportExportOrCondition] 
		[EX] 'by						[NL][IN] 
			[replacement] 					[EX][EX]
	|
	'match [opt dollarStar] [SP] [type]			[NL][IN]
			[pattern] 
		[repeat constructDeconstructImportExportOrCondition] 
end define
	
define ruleFooter
		'end 'rule		 
	|	'end 'function	
end define


define potential_clone
    [ruleStatement]
end define
include "generic-rename-blind.txl"

redefine end_xml_source_coordinate
    [NL] [SPOFF] '</ 'source '> [SPON] [NL]
end redefine
