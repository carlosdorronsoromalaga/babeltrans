<?php
/*
 * Babel Translations — receptor de TODOS los formularios de la web.
 *
 * Sustituye a BreezingForms (Joomla 1.5), que dejó de funcionar con la web.
 * Escrito para PHP 8.x sin librerías: usa mail() del hosting, que en
 * Webempresa funciona tal cual. Manda un e-mail a DESTINO con los campos
 * rellenados y los archivos adjuntos, y devuelve al visitante a la página del
 * formulario con ?enviado=ok o ?enviado=error.
 *
 * Contra el spam: un campo trampa invisible (_web) que solo rellenan los
 * robots, y un tiempo mínimo. El captcha de imagen de la web vieja se quita:
 * molestaba a las personas y ya no paraba a los robots.
 */

declare(strict_types=1);

const DESTINO     = 'info@babeltrans.es';
const REMITENTE   = 'web@babeltrans.es';      // debe ser del propio dominio, o el correo acaba en spam
const MAX_ARCHIVO = 10 * 1024 * 1024;         // 10 MB por archivo
const MAX_TOTAL   = 20 * 1024 * 1024;         // 20 MB entre todos
const EXTENSIONES = ['pdf', 'doc', 'docx', 'odt', 'rtf', 'txt', 'xls', 'xlsx', 'ods', 'ppt', 'pptx',
                     'jpg', 'jpeg', 'png', 'zip', 'mp3', 'wav', 'm4a'];

function volver(string $estado): never
{
    $ruta = $_POST['_volver'] ?? '/';
    // Solo rutas internas: nada de redirigir a otra web
    if (!is_string($ruta) || !preg_match('#^/[A-Za-z0-9/_\-.]*$#', $ruta)) {
        $ruta = '/';
    }
    header('Location: ' . $ruta . '?enviado=' . $estado, true, 303);
    exit;
}

function limpia(string $t): string
{
    return trim(str_replace(["\r", "\0"], '', $t));
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    volver('error');
}

// Robot: rellenó el campo trampa. Se le dice "ok" para que no insista.
if (!empty($_POST['_web'])) {
    volver('ok');
}

$formulario = limpia((string)($_POST['_formulario'] ?? 'Formulario web'));
$idioma     = limpia((string)($_POST['_idioma'] ?? ''));

// Campos: todo lo que no empieza por "_"
$lineas = [];
$correo_visitante = '';
$hay_mail = false;
foreach ($_POST as $nombre => $valor) {
    if (!is_string($nombre) || str_starts_with($nombre, '_')) {
        continue;
    }
    $valor = is_array($valor) ? implode(', ', array_map('strval', $valor)) : (string)$valor;
    $valor = limpia($valor);
    if (strtolower($nombre) === 'mail') {
        $hay_mail = true;
        if (filter_var($valor, FILTER_VALIDATE_EMAIL)) {
            $correo_visitante = $valor;
        }
    }
    $etiqueta = str_replace('_', ' ', $nombre);
    $lineas[] = str_pad($etiqueta . ':', 28) . ($valor === '' ? '—' : $valor);
}

if ($hay_mail && $correo_visitante === '') {
    volver('error');  // el e-mail es obligatorio y tiene que ser válido
}

// Adjuntos
$adjuntos = [];
$total = 0;
foreach ($_FILES as $grupo) {
    $nombres = (array)($grupo['name'] ?? []);
    foreach ($nombres as $i => $nombre_original) {
        $error = ((array)$grupo['error'])[$i] ?? UPLOAD_ERR_NO_FILE;
        if ($error === UPLOAD_ERR_NO_FILE) {
            continue;
        }
        if ($error !== UPLOAD_ERR_OK) {
            volver('error');
        }
        $tmp  = ((array)$grupo['tmp_name'])[$i];
        $peso = (int)((array)$grupo['size'])[$i];
        $ext  = strtolower(pathinfo((string)$nombre_original, PATHINFO_EXTENSION));
        if ($peso > MAX_ARCHIVO || !in_array($ext, EXTENSIONES, true) || !is_uploaded_file($tmp)) {
            volver('error');
        }
        $total += $peso;
        if ($total > MAX_TOTAL) {
            volver('error');
        }
        $seguro = preg_replace('/[^A-Za-z0-9._-]+/', '_', (string)$nombre_original);
        $adjuntos[] = [$seguro, (string)file_get_contents($tmp)];
    }
}

// Mensaje
$asunto = 'Web babeltrans.es · ' . $formulario . ($idioma ? ' [' . strtoupper($idioma) . ']' : '');
$cuerpo = "Nuevo mensaje desde el formulario «{$formulario}» de la web"
        . ($idioma ? " (versión " . strtoupper($idioma) . ")" : '') . ".\n\n"
        . implode("\n", $lineas) . "\n\n"
        . (count($adjuntos) ? 'Adjuntos: ' . count($adjuntos) . "\n" : '')
        . '— ' . date('d/m/Y H:i') . ' · IP ' . ($_SERVER['REMOTE_ADDR'] ?? '?') . "\n";

$frontera = '=_' . bin2hex(random_bytes(12));
$cabeceras = [
    'From: Web Babel Translations <' . REMITENTE . '>',
    'MIME-Version: 1.0',
    'Content-Type: multipart/mixed; boundary="' . $frontera . '"',
];
if ($correo_visitante !== '') {
    $cabeceras[] = 'Reply-To: ' . $correo_visitante;  // validado arriba: sin saltos de línea
}

$mime  = "--{$frontera}\r\n"
       . "Content-Type: text/plain; charset=UTF-8\r\n"
       . "Content-Transfer-Encoding: base64\r\n\r\n"
       . chunk_split(base64_encode($cuerpo)) . "\r\n";
foreach ($adjuntos as [$nombre, $datos]) {
    $mime .= "--{$frontera}\r\n"
           . "Content-Type: application/octet-stream; name=\"{$nombre}\"\r\n"
           . "Content-Transfer-Encoding: base64\r\n"
           . "Content-Disposition: attachment; filename=\"{$nombre}\"\r\n\r\n"
           . chunk_split(base64_encode($datos)) . "\r\n";
}
$mime .= "--{$frontera}--\r\n";

$ok = mail(
    DESTINO,
    '=?UTF-8?B?' . base64_encode($asunto) . '?=',
    $mime,
    implode("\r\n", $cabeceras),
    '-f' . REMITENTE
);

volver($ok ? 'ok' : 'error');
