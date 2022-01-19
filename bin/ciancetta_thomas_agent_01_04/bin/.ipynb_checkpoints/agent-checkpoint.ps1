$u = New-Object -ComObject Microsoft.Update.Session
$u.ClientApplicationID = 'Test Script'
$s = $u.CreateUpdateSearcher()
$r = $s.Search('IsInstalled=0')
$r.updates|select -ExpandProperty Title
exit $LASTEXITCODE