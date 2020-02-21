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
	[ruleHeader]
	[ruleBody]
	[srcfilename] [srclinenumber]
	[ruleFooter]
	|
	%Output form
	[not token]
	[opt xml_source_coordinate]
	[ruleHeader] 
	[ruleBody] [EX] [EX]
	[ruleFooter]
	[opt end_xml_source_coordinate]
end redefine

define ruleHeader
		'rule [ruleid] [repeat formalArgument]	[NL] [IN] [IN]
	| 	'function [ruleid] [repeat formalArgument]	[NL] [IN] [IN]
end define

define ruleBody
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
	
define ruleFooter
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
    	Rules[removeFormatCues]
	                %[removeEmptyStatements]
end function

% It needs to add a [repeat...] in the original txl grammar....
rule removeFormatCues
	replace $ [type]
	_[repeat formatCues]
	by
	% none -removes the formatting cue
end rule

rule convertRuleDefinitions
    % Find each function definition and match its input source coordinates
    replace [ruleStatement]
	FileName [srcfilename] LineNumber [srclinenumber]
	Rule_Header [ruleHeader]
		Rule_Body[ruleBody]
	EndFileName [srcfilename] EndLineNumber [srclinenumber]
    Rule_Footer[ruleFooter]					

	
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
	Rule_Header 
	   Rule_Body  %[unmarkEmbeddedFunctionDefinitions] 
	Rule_Footer
	</source>
end rule

