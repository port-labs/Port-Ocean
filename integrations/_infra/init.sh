if test -e /usr/local/share/ca-certificates/cert.crt; then
  update-ca-certificates
fi

python ./debug.py