kubectl  create namespace flux-system

kubectl  -n flux-system create secret generic sops-age --from-file=age.agekey=./age.txt
