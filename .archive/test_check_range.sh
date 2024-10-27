#!/bin/bash

# Test cases with standard ranges
echo "=== Testing standard version ranges ==="
./scripts/start.sh "hi" ">=1.0.0,<1.1 >=1.0.0,<1.1" "faz-cord faz-db" "WEBHOOK1 WEBHOOK2"
./scripts/start.sh "hi" ">1.0.0,<1.1 >1.0.0,<1.1" "faz-cord faz-db" "WEBHOOK1 WEBHOOK2"

# Test cases with different version numbers
echo -e "\n=== Testing different version numbers ==="
./scripts/start.sh "hi" ">=2.0.0,<3.0 >=2.0.0,<3.0" "faz-cord faz-db" "WEBHOOK1 WEBHOOK2"
./scripts/start.sh "hi" ">=0.9.0,<1.0.0 >=0.9.0,<1.0.0" "faz-cord faz-db" "WEBHOOK1 WEBHOOK2"

# Test cases with patch versions
echo -e "\n=== Testing patch version ranges ==="
./scripts/start.sh "hi" ">=1.0.5,<1.1.0 >=1.0.5,<1.1.0" "faz-cord faz-db" "WEBHOOK1 WEBHOOK2"
./scripts/start.sh "hi" ">1.0.9,<1.2.0 >1.0.9,<1.2.0" "faz-cord faz-db" "WEBHOOK1 WEBHOOK2"

# Test cases with mixed operators
echo -e "\n=== Testing mixed operators ==="
./scripts/start.sh "hi" ">=1.0.0,<=1.1 >=1.0.0,<=1.1" "faz-cord faz-db" "WEBHOOK1 WEBHOOK2"
./scripts/start.sh "hi" ">1.0.0,<=1.1.5 >1.0.0,<=1.1.5" "faz-cord faz-db" "WEBHOOK1 WEBHOOK2"

# Test cases with different services
echo -e "\n=== Testing different service combinations ==="
./scripts/start.sh "hi" ">=1.0.0,<1.1 >=1.0.0,<1.1" "service1 service2" "WEBHOOK1 WEBHOOK2"
./scripts/start.sh "hi" ">=1.0.0,<1.1 >=1.0.0,<1.1" "auth-service data-service" "WEBHOOK1 WEBHOOK2"

# Test cases with major version jumps
echo -e "\n=== Testing major version ranges ==="
./scripts/start.sh "hi" ">=1.0.0,<2.0.0 >=1.0.0,<2.0.0" "faz-cord faz-db" "WEBHOOK1 WEBHOOK2"
./scripts/start.sh "hi" ">=2.0.0,<3.0.0 >=2.0.0,<3.0.0" "faz-cord faz-db" "WEBHOOK1 WEBHOOK2"

# Test cases with different range combinations
echo -e "\n=== Testing different range combinations ==="
./scripts/start.sh "hi" ">=1.0.0,<1.1 >=2.0.0,<2.1" "faz-cord faz-db" "WEBHOOK1 WEBHOOK2"
./scripts/start.sh "hi" ">1.5.0,<2.0 >2.5.0,<3.0" "faz-cord faz-db" "WEBHOOK1 WEBHOOK2"

# Test cases with exact versions
echo -e "\n=== Testing exact version matches ==="
./scripts/start.sh "hi" ">=1.0.0,<=1.0.0 >=1.0.0,<=1.0.0" "faz-cord faz-db" "WEBHOOK1 WEBHOOK2"
./scripts/start.sh "hi" ">=2.1.0,<=2.1.0 >=2.1.0,<=2.1.0" "faz-cord faz-db" "WEBHOOK1 WEBHOOK2"
