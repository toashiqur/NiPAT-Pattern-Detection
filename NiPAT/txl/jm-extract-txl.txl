include "txl.grm"
include "bom.grm"

redefine defineStatement
[empty]
end redefine

redefine redefineStatement
[empty]
end redefine

redefine functionStatement
[empty]
end redefine

redefine ruleStatement
[empty]
end redefine

% Now include all in txlBlock definition...

define txlBlock
	%Input form
	[srcfilename] [srclinenumber]
	[txlBlockHeader] [NL] [IN]
	[txlBlockBody]
	[srcfilename] [srclinenumber]
	[txlBlockFooter]
	|
	%Output form
	[not token]
	[opt xml_source_coordinate]
	[txlBlockHeader] [NL] [IN]
	[txlBlockBody]
	[txlBlockFooter]
	[opt end_xml_source_coordinate]
end define

define txlBlockHeader
		'rule [ruleid] [repeat formalArgument]	
	| 	'function [ruleid] [repeat formalArgument]
	|	'define [typeid]
	|	'redefine [typeid]
end define

define txlBlockBody
		[repeat constructDeconstructImportExportOrCondition] 	
		[EX] [opt skippingType]
		[replace_match] [EX]
	|
		[repeat literalOrType]		[NL] 
		[repeat barLiteralsAndTypes]	[EX][EX] 
	|
		[opt dotDotDotBar] 				% postextension of existing define 
		[repeat literalOrType] 		[NL] 
		[repeat barLiteralsAndTypes]	 
		[opt barDotDotDot] 		[EX][EX]	% preextension of existing define 
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
	
define txlBlockFooter
		'end 'rule		 
	|	'end 'function	
	|	'end 'define 
		[RESET]
	|	'end 'redefine
		[RESET]
end define


%*****************************************************************
define xml_source_coordinate
    '< [SPOFF] 'source [SP] 'file=[stringlit] [SP] 'startline=[stringlit] [SP] 'endline=[stringlit] '> [SPON] [NL]
end define

define end_xml_source_coordinate
    [NL] '< [SPOFF] '/ 'source '> [SPON] [NL]
end define

redefine statement
    ...
    |[txlBlock]
end redefine


redefine program
	...
    | 	[repeat txlBlock]
end redefine


% Main function - extract and mark up rule/function definitions from parsed input program
function main
    replace [program]
	P [program]
    construct txlBlocks [repeat txlBlock]
    	_[^ P] 						% Extract all rules/defines from program
	 [convertBlockDefinitions] 	% Mark up with XML each rule or function
    by 
    	txlBlocks[removeFormatCues]
	                %[removeEmptyStatements]
end function

% It needs to add a [repeat...] in the original txl grammar....
rule removeFormatCues
	replace $ [type]
	_[repeat formatCues]
	by
	% none remove the formatting cue
end rule

rule convertBlockDefinitions
    % Find each function definition and match its input source coordinates
    replace [txlBlock]
	FileName [srcfilename] LineNumber [srclinenumber]
	txl_Block_Header [txlBlockHeader]
	
	    %FunctionBody [repeat declaration_or_statement]	
		txl_Block_Body[txlBlockBody]
		
	EndFileName [srcfilename] EndLineNumber [srclinenumber]	
	txl_Block_Footer[txlBlockFooter]				

	
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
	txl_Block_Header 
	   txl_Block_Body  %[unmarkEmbeddedFunctionDefinitions] 
	txl_Block_Footer
	</source>
end rule

