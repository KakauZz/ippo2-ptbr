# Aplica a traducao do Hajime no Ippo 2 numa COPIA da ISO.
# Uso: clique com o botao direito neste arquivo -> "Executar com o PowerShell"
# A ISO original NAO e alterada.

$ErrorActionPreference = 'Stop'
$pasta   = Split-Path -Parent $MyInvocation.MyCommand.Path
$jogo    = Split-Path -Parent $pasta
$origem  = Join-Path $jogo 'Hajime no Ippo 2 - Victorious Road (Japan).iso'
$destino = Join-Path $jogo 'Hajime no Ippo 2 - Victorious Road (PT-BR).iso'
$novos   = Join-Path $pasta 'arquivos'   # ex.: arquivos\DATA\FIRSTENT.GVX

function LerU32([byte[]]$b, [int]$o) { return [BitConverter]::ToUInt32($b, $o) }
function GravarU32Ambos([byte[]]$b, [int]$o, [uint32]$v) {
    $le = [BitConverter]::GetBytes($v)
    $be = [byte[]]($le[3], $le[2], $le[1], $le[0])
    [Array]::Copy($le, 0, $b, $o, 4)
    [Array]::Copy($be, 0, $b, $o + 4, 4)
}
function LerSetores($fs, [long]$lba, [int]$n) {
    $buf = New-Object byte[] ($n * 2048)
    $fs.Seek($lba * 2048, 'Begin') | Out-Null
    $lidos = 0
    while ($lidos -lt $buf.Length) { $r = $fs.Read($buf, $lidos, $buf.Length - $lidos); if ($r -le 0) { break }; $lidos += $r }
    return ,$buf
}

# Procura um nome num diretorio. Retorna @(lbaDoDir, bufferDoDir, offsetDoRegistro)
function Procurar($fs, [long]$dirLba, [long]$dirTam, [string]$nome) {
    $nSet = [int][Math]::Ceiling($dirTam / 2048)
    $buf = LerSetores $fs $dirLba $nSet
    $o = 0
    while ($o -lt $buf.Length) {
        $len = $buf[$o]
        if ($len -eq 0) { $o = [int](([Math]::Floor($o / 2048) + 1) * 2048); continue }
        $nl = $buf[$o + 32]
        $n = [Text.Encoding]::ASCII.GetString($buf, $o + 33, $nl)
        $n = ($n -split ';')[0].TrimEnd('.')
        if ($n -ieq $nome) { return @($dirLba, $buf, $o) }
        $o += $len
    }
    return $null
}

if (-not (Test-Path $origem)) { throw "Nao achei a ISO original: $origem" }
if (-not (Test-Path $novos))  { throw "Nao achei a pasta de arquivos traduzidos: $novos" }

Write-Host "Copiando a ISO (pode demorar um pouco)..."
Copy-Item $origem $destino -Force

$fs = [IO.File]::Open($destino, 'Open', 'ReadWrite')
try {
    $pvd = LerSetores $fs 16 1
    if ([Text.Encoding]::ASCII.GetString($pvd, 1, 5) -ne 'CD001') { throw 'ISO invalida (sem CD001)' }
    $rootLba = LerU32 $pvd (156 + 2)
    $rootTam = LerU32 $pvd (156 + 10)

    $arquivos = Get-ChildItem $novos -Recurse -File
    foreach ($arq in $arquivos) {
        $rel = $arq.FullName.Substring($novos.Length).TrimStart('\', '/')
        $partes = $rel -split '[\\/]'
        $lba = [long]$rootLba; $tam = [long]$rootTam; $achado = $null
        foreach ($p in $partes) {
            $achado = Procurar $fs $lba $tam $p
            if ($null -eq $achado) { throw "Nao achei '$rel' dentro da ISO" }
            $buf = $achado[1]; $o = $achado[2]
            $lba = [long](LerU32 $buf ($o + 2)); $tam = [long](LerU32 $buf ($o + 10))
        }
        $dirLba = [long]$achado[0]; $dirBuf = $achado[1]; $recOff = $achado[2]
        $dados = [IO.File]::ReadAllBytes($arq.FullName)
        $espaco = [Math]::Ceiling($tam / 2048) * 2048

        if ($dados.Length -le $espaco) {
            $novoLba = [long]$lba
            $modo = 'no lugar'
        } else {
            $fimIso = $fs.Length
            $novoLba = [long][Math]::Ceiling($fimIso / 2048)
            $modo = 'no fim da ISO'
        }
        # grava os dados e completa o setor com zeros
        $pad = [int]([Math]::Ceiling($dados.Length / 2048) * 2048 - $dados.Length)
        $fs.Seek($novoLba * 2048, 'Begin') | Out-Null
        $fs.Write($dados, 0, $dados.Length)
        if ($pad -gt 0) { $z = New-Object byte[] $pad; $fs.Write($z, 0, $pad) }

        # atualiza o registro do diretorio (LBA e tamanho)
        GravarU32Ambos $dirBuf ($recOff + 2)  ([uint32]$novoLba)
        GravarU32Ambos $dirBuf ($recOff + 10) ([uint32]$dados.Length)
        $setor = [int][Math]::Floor($recOff / 2048)
        $fs.Seek(($dirLba + $setor) * 2048, 'Begin') | Out-Null
        $fs.Write($dirBuf, $setor * 2048, 2048)

        Write-Host ("OK: {0} ({1} bytes, {2})" -f $rel, $dados.Length, $modo)
    }

    # atualiza o tamanho total do volume se a ISO cresceu
    $setores = [uint32][Math]::Ceiling($fs.Length / 2048)
    GravarU32Ambos $pvd 80 $setores
    $fs.Seek(16 * 2048, 'Begin') | Out-Null
    $fs.Write($pvd, 0, 2048)
}
finally { $fs.Close() }

Write-Host ""
Write-Host "Pronto! Abra no PCSX2: $destino"
Read-Host "Aperte Enter para fechar"
