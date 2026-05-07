# pizzazz preprocessor
A custom preprocessor for gleam to allow multiline comments, and optionally to use semicolons. Can work directly in any gleam project.
Add to gleam project in a folder sibling to src, and put the file in there, although this is recommended, you may put this file anywhere in the project.
It is by default recursive, to change it, set the value to False in the file
Use the file extension .pizzazz for it to translate it to a .gleam
To use non-space sensitive semicolon mode, start the file with ;
To do multiline comments: /* comment */
I will later make a language server set up for better user experience in an IDE.
