% Blind renaming - txl defines
% Using txl.grm grammar
include "txl.grm"

%Redefine in ruleStatement
redefine functionStatement
[empty]
end redefine


%ReDefinition to include rule, function, replace, match

redefine ruleStatement
	[rule_header] 
	[rule_body] [EX] [EX]
	[rule_footer]
end redefine

define rule_header
		'rule [ruleid] [repeat formalArgument]	[NL] [IN] [IN]
	| 	'function [ruleid] [repeat formalArgument]	[NL] [IN] [IN]
end define

define rule_body
		[repeat constructDeconstructImportExportOrCondition] 	
		[EX] [opt skippingType]
		[replace_match]
end define

define replace_match
	'replace [opt dollarStar] [SP] [type]			[NL][IN] 
			[pattern]
		[repeat constructDeconstructImportExportOrCondition] 
		[EX] 'by						[NL][IN] 
			[replacement] 				
	|
	'match [opt dollarStar] [SP] [type]			[NL][IN]
			[pattern] 
		[repeat constructDeconstructImportExportOrCondition] 
end define
	
define rule_footer
		'end 'rule	 
	|	'end 'function
end define


define potential_clone
    [ruleStatement]
end define
include "generic-shortform-normalize-tolongform.txl"

redefine end_xml_source_coordinate
    [NL] [SPOFF] '</ 'source '> [SPON] [NL]
end define
