# download
mkdir -p pile
cd pile
for i in $(seq 0 9)
    do wget https://mystic.the-eye.eu/public/AI/pile/train/0$i.jsonl.zst
done

for i in $(seq 10 29)
    do wget https://mystic.the-eye.eu/public/AI/pile/train/$i.jsonl.zst
done

# decompress
for i in $(seq 0 9)
    do zstd -d --rm 0$i.jsonl.zst
done

for i in $(seq 10 29)
    do zstd -d --rm $i.jsonl.zst
done

cd -
