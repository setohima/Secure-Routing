import java.io.*; 
import java.net.*;
public class GossipServer 
{ 
public static void main(String[] args) throws Exception
 { 
ServerSocket sersock = new ServerSocket(3000);
System.out.println("NODE READY FOR KEY EXCHANGE");
Socket sock = sersock.accept( ); // reading from keyboard (keyRead object)
BufferedReader keyRead =new BufferedReader(new InputStreamReader(System.in)); // sending to client (pwrite object) 
OutputStream ostream =sock.getOutputStream();
PrintWriter pwrite =new PrintWriter(ostream, true); // receiving from server ( receiveRead object)
InputStream istream =sock.getInputStream(); 
BufferedReader receiveRead =new BufferedReader(new InputStreamReader(istream)); 
String receiveMessage;
String sendMessage;
String sendMessage1;
int xb=10;
int alpha=7;
int q=71;
int k=0;
int a=1;
while(a<3) 
{
 if((receiveMessage = receiveRead.readLine()) != null) 
{ 
  int cal=Integer.parseInt(receiveMessage);
   k=cal^xb;
  
 } 
int yb=(((alpha)^xb)%q);
sendMessage =Integer.toString(yb);
sendMessage1 =Integer.toString(k);
 pwrite.println(sendMessage);
 pwrite.println(sendMessage1);
 System.out.flush();
a++;
}
System.out.println("Computed K Value :"+k); 
} 
} 
