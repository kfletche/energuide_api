import express from 'express'
import bodyParser from 'body-parser'
import cors from 'cors'
import { graphqlExpress, graphiqlExpress } from 'apollo-server-express'
import Schema from './schema'
import { i18n, unpackCatalog } from 'lingui-i18n'
import requestLanguage from 'express-request-language'

i18n.load({
  fr: unpackCatalog(require('./locale/fr/messages.js')),
  en: unpackCatalog(require('./locale/en/messages.js')),
})

function Server(context = {}, ...middlewares) {
  const server = express()
  middlewares.forEach(middleware => server.use(middleware))
  server
    .use(
      requestLanguage({
        languages: i18n.availableLanguages.sort(),
      }),
    )
    .use(cors())
    .use(
      '/graphql',
      bodyParser.json(),
      graphqlExpress(request => {
        i18n.activate(request.language)
        return {
          schema: new Schema(i18n),
          context,
          tracing: true,
          cacheControl: true,
        }
      }),
    )
  server.get('/graphiql', graphiqlExpress({ endpointURL: '/graphql' }))
  server.get('/', function(req, res) {
    res.redirect('/graphiql')
  })
  server.get('/alive', (req, res) => {
    res.send('yes')
  })
  server.get('/ready', async (req, res) => {
    try {
      const result = await context.client.findOne()
      if (result) {
        res.send('yes')
      } else {
        res.status(500).json({
          error: 'Database check failed. No data returned.',
        })
      }
    } catch (error) {
      res.status(500).json({ error: error.toString() })
    }
  })
  return server
}

export default Server
