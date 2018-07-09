<?php 
if(isset($_POST['personName'])&&isset($_POST['personFormEmail'])&&isset($_POST['FormComment']))
{
    $name=trim($_POST['personName']);
    $email=trim($_POST['personFormEmail']);
    $comment=trim($_POST['FormComment']);
    
    if($name !== "" && $email !== "" && $comment !== "")
    {
	    $message="Hi, I'm $name\n\n. $comment. \n\nSender's Contact: $email";
	    @mail( 'trmughilan@gmail.com', 'This is the message from Skylark Website', $message);
        @mail( 'mrinalpai92@gmail.com', 'This is the message from Skylark Website', $message);
        echo "<html>
        <head>
            <title>Contact Us</title>
            <link rel=\"stylesheet\" href=\"css/main.css\" />
        </head>
        <body>
            <center style=\"position: absolute; top: 44%; right: 40%\">
                <h1>Thank You </h1>
                <a href = \"http://skylarkdrones.com\">Go Back to SkylarkDrones.com</a>
            </center>
        </body>
    </html>";
    }
    else
    {
         echo "<html>
        <head>
            <title>Contact Us</title>
            <link rel=\"stylesheet\" href=\"css/main.css\" />
        </head>
        <body>
            <center style=\"position: absolute; top: 44%; right: 40%\">
                <h1>Please fill in all the details</h1>
                <a href = \"http://skylarkdrones.com#contact\">Go Back to SkylarkDrones.com/custom.html</a>
            </center>
        </body>
    </html>";
    }
}
?>
