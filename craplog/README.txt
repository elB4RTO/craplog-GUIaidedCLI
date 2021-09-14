  ----------------------------------------------------------- 
 ¦                                                           ¦
 ¦     A tool that scrapes Apache2 default log files and     ¦
 ¦     creates both SINGLE-SESSION and GLOBAL statistics     ¦
 ¦                                                           ¦
 ¦===========================================================¦
 ¦                                                           ¦
 ¦  USAGE:                                                   ¦
 ¦                                                           ¦
 ¦  ./craplog.sh [ARGUMENTS]                                 ¦
 ¦                                                           ¦
 ¦===========================================================¦
 ¦                                                           ¦
 ¦  ARGUMENTS:                                               ¦
 ¦                                                           ¦
 ¦     --help      ¦ print this screen and exit              ¦
 ¦-----------------------------------------------------------¦
 ¦     --less      ¦ less output on screen                   ¦
 ¦-----------------------------------------------------------¦
 ¦     --clean     ¦ create a cleaned access.log.1 file      ¦
 ¦-----------------------------------------------------------¦
 ¦    --errors     ¦ make statistics of error.log.1 file too ¦
 ¦-----------------------------------------------------------¦
 ¦  --only-errors  ¦ use only error logs (skip access logs)  ¦
 ¦-----------------------------------------------------------¦
 ¦ --only-globals  ¦ only update globals (skip session stats)¦
 ¦-----------------------------------------------------------¦
 ¦ --avoid-globals ¦ do not update global statistics         ¦
 ¦-----------------------------------------------------------¦
 ¦    --backup     ¦ create a backup archive with originals  ¦
 ¦-----------------------------------------------------------¦
 ¦ --backu+delete  ¦ create a backup + delete original files ¦
 ¦-----------------------------------------------------------¦
 ¦  --auto-delete  ¦ auto-delete files when needed           ¦
 ¦-----------------------------------------------------------¦
 ¦    --trash      ¦ move files to Trash instead of remove   ¦
 ¦-----------------------------------------------------------¦
 ¦    --shred      ¦ use shred on files instead of remove    ¦
  ----------------------------------------------------------- 
