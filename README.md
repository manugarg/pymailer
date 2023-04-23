One of the earliest open source tools I wrote, in 2005. Imported it from [sf.net](https://sourceforge.net/projects/pymailer/) just for memorabilia :-)

--------


<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<body style='font-size:10.0pt;font-family:Helvetica'>
<h1>About pyMailer</h1>
pyMailer
is a cute little app which strives to do just one thing well.
That
one thing is sending mails. pyMailer is written in python which
automatically provides for platform independence.<br>
<br>
<h2>Installation</h2>
pyMailer
comes in 2 packages:<br>
-
python scripts and <br>
-
win32 executables created by py2exe. <br>
<br>
To
run scripts version, you need python 2.2 or higher version.
Installation is pretty simple: just download the zipped files and
extract to
some directory. You can run 'installsendto' to add a link to pymailer
in SendTo on windows. This comes pretty handy for sending files quickly.<br>
<br>
<h2>Usage</h2>
<h3>Command
Line Version:</h3>
It's
mostly meant for unix. (who uses commands on windows anyways ;-)). <br>
<pre style="font-family: monospace;">
Usage: pymailer.py [options] to [to ...]*

Options:
    -h, --help  Print this message and exit.

    -a          Attachment. Use multiple '-a' options to attach multiple files
    -s,--subject
                Subject
    -f,--from   Fromaddr
    --smtpstr   Smtp string in the format 'server:port|encrypt|user|password'
    --smtpsvr   Smtp server in the format server:port.
                All other fields are considered empty in smtpstr

`to' is the email address of the recipient of the message, and multiple
recipients may be given.
</pre>
<b>Examples:</b><br>
<br>
<i>To send using local smtp server-</i>

```shell
python pymailer.py -s "system configuration file" -a /etc/sysctl.conf \
    -f root manugarg@gmail.com < /dev/null
```

<i>To send using your company's smtp server -</i>

```shell
python pymailer.py -s "System logs" -a /var/log/messeges -f root --smtpsvr \
    "smtp.yourcompany.com:25" manugarg@gmail.com < /dev/null
```

<i>To send using gmail's smtp server -</i>

```shell
python pymailer.py -s "other mail" -a $HOME/notes -f manugarg@gmail.com --smtpstr \
    "smtp.gmail.com:587|TLS|manugarg@gmail.com|mypassword" \
    manu.garg@work.com < /dev/null
```

### Graphical Interface

This version has rather more features and as a matter of fact I started
writing this first and command line version was a side product of
development of this version.

```
python pymailerw.py [file1] [file2] ... 
# or, if you are using executables on windows
pymailerw.exe [file1] [file2] ...
```

</span>First run:<br>
<br>
<img style="width: 640px; height: 349px;"
 alt="First run with no saved configuration"
 src="https://sourceforge.net/dbimage.php?id=30074">
<br>
<br>
This
shows the screenshot of the first run, with no saved configuration. You
can
specify recepeints in by checking the &lsquo;Others&rsquo; box
or you can configure 'Contacts' list for quick selection.&nbsp; To
be able to send
mail you need to configure some SMTP options first.<br>
<br>
<span style="font-weight: bold;">Editing
Send Options</span>:<br>
<br>
This
version reads sending
options from a configuration file which is stored in
your profile directory. You can edit this file directly from the main
window by clicking 'Edit Send Options' button. This opens up a new
window in which you can add/edit smtp options. You specify smtp options
using the same smtp string format. We'll talk more about smtp string in
coming section.<br>
<br>
<img style="width: 640px; height: 443px;" alt="Editing send options"
 src="https://sourceforge.net/dbimage.php?id=30080"><br>
<br>
Once you are finished with editing, save the file and exit. To effect
the changes, you will have to click on 'Reload' button on main
screen.<br>
<br>
<span style="font-weight: bold;">Editing
Contacts</span>:<br>
<br>
This is not a requirement, but it comes handy when you send mails to
same email addresses frequently. This configuration is also stored in a
file. To edit this file click on 'Edit Contacts'. It will pop up a
window where you can edit these options.<br>
<br>
<br>
<img style="width: 620px; height: 479px;" alt="Editing Contacts"
 src="https://sourceforge.net/dbimage.php?id=30078"><br>
<br>
First 5 contacts from this file, appear on main window. Rest you can
select by clicking on 'Find' button next to 'Others' textbox.<br>
<br>
All of these configurations are saved in you profile directory. Next time when
you open pymailerw, these configurations are automatically read and
resulting window looks something like below:<br>
<br>
<img style="width: 640px; height: 349px;" alt="With saved configuration"
 src="https://sourceforge.net/dbimage.php?id=30082"><br>
<br>
If you specify a filename at command line, that will appear inside
&lsquo;File&rsquo; textbox
and file name is automatically added to
the &lsquo;Subject&rsquo; field. This is what happens when you
send a file using 'SendTo' list in Windows.<br>
<br>

<h3>SMTP String</h3>
SMTP string is ubiquitous in pyMailer. It&rsquo;s a convenient
way to specify smtp options. <br>
<br>
<b>'server:port|encrypt|user|password'</b>
<br>
<br>
<table style="font-size:10.0pt;font-family:Helvetica; text-align: left; width: 100%;" border="1" cellpadding="2"
 cellspacing="2">
  <tbody>
    <tr>
      <td>server:port</td>
      <td>SMTP server and port. If
this field is left empty, it is assumed to be local server.</td>
    </tr>
    <tr>
      <td>encrypt</td>
      <td>Specifies if SMTP server
uses encryption. If this field is empty, no encryption is used.
Currently only &lsquo;TLS&rsquo; encryption is supported.</td>
    </tr>
    <tr>
      <td>user</td>
      <td>It specifies username if
server requires authentication. If this field is
empty, no authentication is used.</td>
    </tr>
    <tr>
      <td>password</td>
      <td>Password if
authentication is required. If this field is empty and
&lsquo;user&rsquo; is non-empty,
user is prompted for the password before sending mail.</td>
    </tr>
  </tbody>
</table>
<br>
<h3>Questions/Suggestions/Bugs</h3>
<p>I can be reached at manugarg at gmail dot com. 
I'll be pleased to help you with anything related to pymailer.</p>
</body>
</html>

