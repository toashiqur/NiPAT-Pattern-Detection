include "txl.grm"
include "bom.grm"

redefine redefineStatement
[empty]
end redefine

%ReDefinition to include define, redefine

redefine defineStatement
	%Input form
	[srcfilename] [srclinenumber]
	[define_header]
	[define_body]
	[srcfilename] [srclinenumber]
	[define_footer]
	|
	%Output form
	[not token]
	[opt xml_source_coordinate]
	[define_header]
	[define_body]
	[define_footer]
	[opt end_xml_source_coordinate]
end redefine

define define_header
		'define [typeid] [NL][IN][IN]
	|	'redefine [typeid] [NL][IN][IN]
end define

define define_body
		[repeat literalOrType]		%[NL] ++++++++--------
		[repeat barLiteralsAndTypes]	[EX][EX]
	|
		[opt dotDotDotBar] 				% postextension of existing define 
		[repeat literalOrType] 		%[NL] ++++++--------
		[repeat barLiteralsAndTypes]	 
		[opt barDotDotDot] 		[EX][EX]	% preextension of existing define 
end define

	
define define_footer
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
    	Defines   %[removeOptSemis]
	                %[removeEmptyStatements]
end function


rule convertDefineDefinitions
    % Find each function definition and match its input source coordinates
    replace [defineStatement]
	FileName [srcfilename] LineNumber [srclinenumber]
	DefineHeader [define_header]
		DefineBody[define_body]
   EndFileName [srcfilename] EndLineNumber [srclinenumber]
	DefineFooter[define_footer]			
			

	
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
	DefineHeader 
	   DefineBody  %[unmarkEmbeddedFunctionDefinitions] 
	DefineFooter
	</source>
end rule

