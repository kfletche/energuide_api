[La version française suit.](#---------------------------------------------------------------------)

# NRCAN's Energuide API

CircleCI Status: [![CircleCI](https://circleci.com/gh/cds-snc/nrcan_api.svg?style=svg)](https://circleci.com/gh/cds-snc/nrcan_api)

This is the API for NRCAN's Energuide data.

## Running the server

#### Quickstart

```sh
# make sure to set your NRCAN_ENGINE_API_KEY environment variable
export NRCAN_ENGINE_API_KEY=your_apollo_engine_api_key

# build and run the API
make watch
```

`make watch` will do a few things for you
- install all missing dependencies
- build the app
- serve the API locally
- rebuild and restart if you make any changes

Once it's running, check it out at [http://localhost:3000/](http://localhost:3000/).
Or [here's an example query](http://localhost:3000/graphiql?query=%7B%0A%20%20dwellings(%0A%20%20%20%20filters%3A%20%5B%0A%20%20%20%20%20%20%7Bfield%3A%20dwellingForwardSortationArea%20comparator%3A%20eq%20value%3A%20%22C1A%22%7D%0A%20%20%20%20%5D%0A%20%20)%20%7B%0A%20%20%20%20results%20%7B%0A%20%20%20%20%20%20yearBuilt%0A%20%20%20%20%20%20city%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D) to get you going.

### Manually starting the server

Running the sever requires a MongoDB server running somewhere and the following environmental variables defined:

* NRCAN_ENGINE_API_KEY
* NRCAN_DB_CONNECTION_STRING
* NRCAN_DB_NAME
* NRCAN_COLLECTION_NAME

With those defined you can run the server like this:

```sh
> yarn && yarn run build
> NRCAN_DB_CONNECTION_STRING="mongodb://localhost:27017" \
	NRCAN_DB_NAME="energuide" \
	NRCAN_COLLECTION_NAME="dwellings" \
	NRCAN_ENGINE_API_KEY="your_apollo_engine_api_key" yarn start
```

The API server is available as a Docker container and can be run with:
```
docker run -it -e "NRCAN_ENGINE_API_KEY=your_apollo_engine_api_key" -e "NRCAN_DB_CONNECTION_STRING=mongodb://localhost:27017" -e "NRCAN_DB_NAME=energuide" -e "NRCAN_COLLECTION_NAME=dwellings" --net="host" -p 3000:3000 cdssnc/nrcan_api

```

The container will need network connectivity to the database (obviously) so
ensure that docker networking is setup up in such a way to allow that. The
above command uses the `--net="host"` option to connect the container to the
SQLServer database installed on the host machine. Adjust as needed.
Monitoring and caching is done with [Apollo Engine](https://engine.apollographql.com), hence the API key.

Assuming the DB credentials/connectivity is correct, the command above will
start a graphql endpoint that will respond to the following `curl` commands:

```sh
curl -s -H "Content-Type: application/json" -d '{"query": "{dwellings(filters: [{field: dwellingForwardSortationArea comparator: eq value: \"C1A\"}]){ results { yearBuilt city }}}"}'  "localhost:3000/graphql"
```

It is also possible to access the API via `/graphiql` which will serve up a Graphical IDE to allow you to explore the functionality the API offers and run queries against it.

## Running the tests

Run the unit tests

```sh
yarn test
```

Run the integration tests

```sh
yarn integration
```
## ---------------------------------------------------------------------

# API Énerguide de RNCAN

Statut de CircleCI : [![CircleCI](https://circleci.com/gh/cds-snc/nrcan_api.svg?style=svg)](https://circleci.com/gh/cds-snc/nrcan_api)

Voici le API pour les données du Énerguide de RNCAN.

## Faire fonctionner le serveur

#### Démarrage rapide

```sh
# assurez-vous d'identifier la variable d'environnement NRCAN_ENGINE_API_KEY
export NRCAN_ENGINE_API_KEY=your_apollo_engine_api_key

# Construire et exécuter l'API
make watch
```

`make watch` fera plusieurs choses pour vous
- installera les dépendances manquantes
- Construire l'application
- servir l'API localement
- reconstruire et redémarrer si vous faites des changements

Une fois exécuter, visitez au [http://localhost:3000/](http://localhost:3000/).
Ou [voici un exemple de requête](http://localhost:3000/graphiql?query=%7B%0A%20%20dwellings(%0A%20%20%20%20filters%3A%20%5B%0A%20%20%20%20%20%20%7Bfield%3A%20dwellingForwardSortationArea%20comparator%3A%20eq%20value%3A%20%22C1A%22%7D%0A%20%20%20%20%5D%0A%20%20)%20%7B%0A%20%20%20%20results%20%7B%0A%20%20%20%20%20%20yearBuilt%0A%20%20%20%20%20%20city%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D) pour vous aider à commencer.

### Démarrer le serveur manuellement

Rouler le serveur requiert qu'un serveur MongoDB soit actif avec les variables environnementales définies suivantes :

* NRCAN_ENGINE_API_KEY
* NRCAN_DB_CONNECTION_STRING
* NRCAN_DB_NAME
* NRCAN_COLLECTION_NAME

Avec ces variables définies vous pouvez exécuter le serveur de cette façon :

```sh
> yarn && yarn run build
> NRCAN_DB_CONNECTION_STRING="mongodb://localhost:27017" \
	NRCAN_DB_NAME="energuide" \
	NRCAN_COLLECTION_NAME="dwellings" \
	NRCAN_ENGINE_API_KEY="your_apollo_engine_api_key" yarn start
```

Le serveur de l'API est disponible en tant que conteneur Docker et peut être exécuter de cette façon :
```
docker run -it -e "NRCAN_ENGINE_API_KEY=your_apollo_engine_api_key" -e "NRCAN_DB_CONNECTION_STRING=mongodb://localhost:27017" -e "NRCAN_DB_NAME=energuide" -e "NRCAN_COLLECTION_NAME=dwellings" --net="host" -p 3000:3000 cdssnc/nrcan_api

```

Le conteneur aura besoin d'une connection réseau vers la base de données donc veuillez vous assurer que le réseautage docker soit configurer en conséquence. La commande ci-dessus utilise l'option `--net="host"` pour connecter le conteneur à la base de données SQLServer installée sur la machine hôte. Ajustez au besoin.
La surveillance et le caching sont effectués avec [Apollo Engine](https://engine.apollographql.com), le pourquoi de la clé API.

Assumant que les authentifiants et la connectivité fonctionnent, la commande ci-dessus va démarrer un 'endpoint' graphql qui répondra au commande `curl` suivantes :

```sh
curl -s -H "Content-Type: application/json" -d '{"query": "{dwellings(filters: [{field: dwellingForwardSortationArea comparator: eq value: \"C1A\"}]){ results { yearBuilt city }}}"}'  "localhost:3000/graphql"
```

C'est aussi possible d'accéder au API à partir du dossier `/graphiql` qui servira une interface graphique qui vous permettra d'explorer les fonctionnalités qu'offre l'API et y exécuter des requêtes.

## Exécuter les tests

Exécuter les tests unitaires

```sh
yarn test
```

Exécuter les test d'intégration

```sh
yarn integration
```
