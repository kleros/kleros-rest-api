## T2CR Endpoints

These endpoints are for the Kleros Token^2 Curated Registry (https://tokens.kleros.io)

These endpoints caches results for an 10 minutes. For real time data use the blockchain directly.

### GET `/t2cr/tokens`

This endpoint fetches tokens in the Kleros T2CR. Here are the different query params to tailor your request:

| Query Parameter                 | Description                                                       | Example                                                     |
|---------------------------------|-------------------------------------------------------------------|-------------------------------------------------------------|
| registered <default=true>: bool | Returns Tokens registered in the list                             | https://api.kleros.io/t2cr/tokens?registered=true         |
| absent: bool                    | Returns Tokens rejected from the list                             | https://api.kleros.io/t2cr/tokens?absent=true             |
| requested: bool                 | Returns Tokens requested to be added to the list                  | https://api.kleros.io/t2cr/tokens?requested=true          |
| clearing: bool                  | Returns Tokens requested to be removed from the list              | https://api.kleros.io/t2cr/tokens?clearing=true           |
| disputed: bool                  | Returns Tokens currently in a dispute to be added to the list     | https://api.kleros.io/t2cr/tokens?disputed=true           |
| clearing_disputed: bool        | Returns Tokens currently in a dispute to be removed from the list  | https://api.kleros.io/t2cr/tokens?clearing_disputed=true  |
| erc20 <default=false>: bool     | Return Tokens that have the ERC20 badge                           | https://api.kleros.io/t2cr/tokens?erc20=true              |
