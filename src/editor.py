import cgi
form=cgi.FieldStorage()
print "Content-Type: text/html\n"
print """<!DOCTYPE html>
<html lang="en">

<head>
    <title>CodeBin</title>
    <link rel="stylesheet" type="text/css" href="./css/editor.css"/>

    <link rel="stylesheet" rel="stylesheet" type="text/css" media="screen" href="http://openfontlibrary.org/face/hans-kendrick"/>
    <link rel="stylesheet" href="./bin/icons/font-awesome-4.0.3/css/font-awesome.min.css"/>


    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js" type="text/javascript"></script> 
    <script src="./js/skulpt.min.js" type="text/javascript"></script> 
    <script src="./js/skulpt-stdlib.js" type="text/javascript"></script> 
    <script type="text/javascript">
      //Skeleton for loading the python code from a .txt file
      function LoadPython()
      {
        xmlhttp=new XMLHttpRequest();
        xmlhttp.onreadystatechange=function()
        {
          if (xmlhttp.readyState==4 && xmlhttp.status==200)
          {
            document.getElementById("editor").innerHTML=xmlhttp.responseText;
          }
          else if (xmlhttp.status==404)
          {
            document.getElementById("editor").innerHTML="Error.";
          }
        }
"""
try:
  print "xmlhttp.open('GET','backend.py?file="+form['scriptName'].value+"',true);"
except:
  print """xmlhttp.open("GET","backend.py",true);"""
print """
        xmlhttp.send();
      }
    </script> 
</head>"""
try:
  form['scriptName'].value
  print "<body onload='LoadPython();'>"
except:
  print "<body>"
print """
<body>

  <script type="text/javascript"> 
    // output functions are configurable.  This one just appends some text
    // to a pre element.
    function outf(text) { 
        var mypre = document.getElementById("output"); 
        mypre.innerHTML = mypre.innerHTML + text; 
    } 
    function builtinRead(x) {
        if (Sk.builtinFiles === undefined || Sk.builtinFiles["files"][x] === undefined)
                throw "File not found: '" + x + "'";
        return Sk.builtinFiles["files"][x];
    }
     
    // Here's everything you need to run a python program in skulpt
    // grab the code from your textarea
    // get a reference to your pre element for output
    // configure the output function
    // call Sk.importMainWithBody()
    function runit() { 
       var prog = editor.getSession().getValue(); 
       var mypre = document.getElementById("output"); 
       mypre.innerHTML = ''; 
       Sk.canvas = "mycanvas";
       Sk.pre = "output";
       Sk.configure({output:outf, read:builtinRead}); 
       eval(Sk.importMainWithBody("<stdin>",false,prog)); 
    } 
  </script> 
 

  <div id="header-content">
    <h1 id="logo">CodeBin</h1>

  </div>

  <div id="body-content">
      <form id="body-form">  
        <div id="editor">print "Hello World!"</div>
        <div id="output">
          <canvas id="mycanvas" ></mycanvas> 
        </div>
        <button type="button" onclick="runit()">Run</button> 
      </form>  
  </div>

  <script src="./bin/libraries/ace-builds-master/src-noconflict/ace.js" type="text/javascript" charset="utf-8"></script>
  <script>
      var editor=ace.edit("editor");
      editor.setTheme("ace/theme/tomorrow_night");
      editor.getSession().setMode("ace/mode/python");
      editor.setFontSize(12);
 	</script>	

</body>

</html>"""