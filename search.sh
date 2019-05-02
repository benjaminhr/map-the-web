#/usr/bin/env sh

url=$1

data="$(curl --silent $url)"
urls=$(echo $data | grep -Eo "(http|https)://[a-zA-Z0-9./?=_-]*" | sort | uniq)
echo "$urls"