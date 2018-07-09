<?php 
if(isset($_POST['feedbackFormName'])&&isset($_POST['feedbackFormEmail'])&&isset($_POST['feedbackFormComment']))
{
    $name=trim($_POST['feedbackFormName']);
    $email=trim($_POST['feedbackFormEmail']);
    $comment=trim($_POST['feedbackFormComment']);
    
    if($name !== "" && $email !== "" && $comment !== "")
    {
	    $message="This is a message left by a visitor at your Website.\n\n Hi, I'm $name,\n\n. $comment. \n\nSender's Contact: $email";
	    
        @mail( 'info@skylarkdrones.com', 'This is the message from Skylark Website', $message);
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
                <a href = \"http://skylarkdrones.com#contact\">Go Back to SkylarkDrones.com/CONTACT</a>
            </center>
        </body>
    </html>";
    }
}
?>
