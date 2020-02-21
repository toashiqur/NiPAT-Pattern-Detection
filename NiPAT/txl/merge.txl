include "txl.grm"

rule main
   replace [repeat statement]
       'include FileName [stringlit]
       RestOfStatements [repeat statement]

	import TXLargs[repeat stringlit]
	deconstruct * TXLargs
	"-path" pathName[stringlit] otherOption[repeat stringlit]		   

	   construct File[stringlit]
	   pathName[+FileName]	  
	
   construct FileContents [repeat statement]
       _ [read File]
   by
       FileContents [. RestOfStatements]

end rule