
New-SelfSignedCertificate -CertStoreLocation cert:\currentuser\my -Subject "CN=Test Code Signing" -KeyAlgorithm RSA -KeyLength 2048 -Provider "Microsoft Enhanced RSA and AES Cryptographic Provider" -KeyExportPolicy Exportable -KeyUsage DigitalSignature -Type CodeSigningCert

certutil -encode '.\cert.pfx' 'cert_base64.txt'
certutil -decode 'cert_base64.txt' '.\cert_new.pfx'

certutil -f -p "supersafepassword" -importpfx .\cert_new.pfx