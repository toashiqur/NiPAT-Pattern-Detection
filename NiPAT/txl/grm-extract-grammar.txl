include "txl.grm"
include "bom.grm"

redefine redefineStatement
[empty]
end redefine

%ReDefinition to include define, redefine

redefine defineStatement
	%Input form
	[srcfilename] [srclinenumber]
	[defineHeader]
	[defineBody]
	[srcfilename] [srclinenumber]
	[defineFooter]
	|
	%Output form
	[not token]
	[opt xml_source_coordinate]
	[defineHeader]
	[defineBody]
	[defineFooter]
	[opt end_xml_source_coordinate]
end redefine

define defineHeader
		'define [typeid] [NL][IN][IN]
	|	'redefine [typeid] [NL][IN][IN]
end define

define defineBody
		[repeat literalOrType]		[NL] %++++++++--------
		[repeat barLiteralsAndTypes]	[EX][EX]
	|
		[opt dotDotDotBar] 				% postextension of existing define 
		[repeat literalOrType] 		[NL] %++++++--------
		[repeat barLiteralsAndTypes]	 
		[opt barDotDotDot] 		[EX][EX]	% preextension of existing define 
end define

	
define defineFooter
		'end 'define
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

redefine program
	...
    | 	[repeat defineStatement]
end redefine

% Main function - extract and mark up rule/function definitions from parsed input program
function main
    replace [program]
	P [program]
    construct Defines [repeat defineStatement]
    	_ [^ P] 			% Extract all Defines/Redefines from program
	 [convertDefineDefinitions] 	% Mark up with XML each rule or function
    by 
    	Defines[removeFormatCues]
	                %[removeEmptyStatements]
end function

% It needs to add a [repeat...] in the original txl grammar....
rule removeFormatCues
	replace $ [type]
	_[repeat formatCues]
	by
	% none -removes the formatting cue
end rule

rule convertDefineDefinitions
    % Find each function definition and match its input source coordinates
    replace [defineStatement]
	FileName [srcfilename] LineNumber [srclinenumber]
	Define_Header [defineHeader]
		Define_Body[defineBody]
   EndFileName [srcfilename] EndLineNumber [srclinenumber]
	Define_Footer[defineFooter]			
			

	
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
	Define_Header 
	   Define_Body  %[unmarkEmbeddedFunctionDefinitions] 
	Define_Footer
	</source>
end rule

