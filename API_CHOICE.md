# API Choice

- Étudiant : Tom VACHER
- API choisie : Quotable
- URL base : https://api.quotable.io/
- Documentation officielle / README : https://github.com/lukePeavey/quotable
- Auth : None
- Endpoints testés :
  - `GET /random` (Citations aléatoires)
  - `GET /quotes` (Liste paginée des citations)
  - `GET /authors` (Liste des auteurs)
  - `GET /search/quotes` (Recherche)
  - `GET /nonexistent` (Endpoint inexistant pour test 404)
- Hypothèses de contrat (champs attendus, types, codes) :
  - `/random` : 200 OK, retourne un objet avec `_id` (string), `content` (string), `author` (string), `tags` (list), `length` (int).
  - `/quotes` : 200 OK, retourne un objet avec `results` (array), `count` (int), `totalPages` (int).
- Limites / rate limiting connu : Non documenté explicitement mais généralement 150-180 requêtes / minute.
- Risques (instabilité, downtime, CORS, etc.) : Risque de ralentissement ponctuel si le service est hébergé sur une instance libre.
