<?php

$arquivo = __DIR__ . "/fiis.py";

chmod($arquivo,777);

//  python3 /var/www/python/investimentos/fii/fiis.py 'HGRU11 XPLG11 BCFF11 KNRI11 XPML11 MXRF11 VINO11 RECT11 MORE11 RBFF11 RBVA11 HTMX11'

$comando = "python3 " . $arquivo . " 'HGRU11 XPLG11 BCFF11 KNRI11 XPML11 MXRF11 VINO11 RECT11 MORE11 RBFF11 RBVA11 HTMX11' ";

echo shell_exec($comando." 2>&1");