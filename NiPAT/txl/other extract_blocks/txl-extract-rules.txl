include "txl.grm"
include "bom.grm"

%Redefine in ruleStatement
redefine functionStatement
[empty]
end redefine

%ReDefinition to include rule, function, replace, match

redefine ruleStatement
	%Input form
	[srcfilename] [srclinenumber]
	[rule_header]
	[rule_body]
	[srcfilename] [srclinenumber]
	[rule_footer]
	|
	%Output form
	[not token]
	[opt xml_source_coordinate]
	[rule_header] 
	[rule_body] [EX] [EX]
	[rule_footer]
	[opt end_xml_source_coordinate]
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


%*****************************************************************
define xml_source_coordinate
    '< [SPOFF] 'source [SP] 'file=[stringlit] [SP] 'startline=[stringlit] [SP] 'endline=[stringlit] '> [SPON] [NL]
end define

define end_xml_source_coordinate
    [NL] '< [SPOFF] '/ 'source '> [SPON] [NL]
end define

redefine program
	...
    | 	[repeat ruleStatement]
end redefine

% Main function - extract and mark up rule/function definitions from parsed input program
function main
    replace [program]
	P [program]
    construct Rules [repeat ruleStatement]
    	_ [^ P] 			% Extract all rules/functions from program
	 [convertRuleDefinitions] 	% Mark up with XML each rule or function
    by 
    	Rules   %[removeOptSemis]
	                %[removeEmptyStatements]
end function


rule convertRuleDefinitions
    % Find each function definition and match its input source coordinates
    replace [ruleStatement]
	FileName [srcfilename] LineNumber [srclinenumber]
	RuleHeader [rule_header]
		RuleBody[rule_body]
	EndFileName [srcfilename] EndLineNumber [srclinenumber]
    RuleFooter[rule_footer]					

	
    % Convert file name and line numbers to strings for XML
    construct FileNameString [stringlit]
	_ [quote FileName] 
    construct LineNumberString [stringlit]
	_ [quote LineNumber] 
    construct EndLineNumberString [stringlit]
	_ [quote EndLineNumber] 
	

    % Output is XML form with attributes indicating input source coordinates
    construct XmlHeader [xml_source_coordinate]
	<source file=FileNameString startline=LineNumberString endline=EndLineNumberString>
    by
	XmlHeader
	RuleHeader 
	   RuleBody  %[unmarkEmbeddedFunctionDefinitions] 
	RuleFooter
	</source>
end rule

