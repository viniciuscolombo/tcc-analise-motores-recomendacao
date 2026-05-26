import http from 'k6/http';
import { check, sleep } from 'k6';
import { Trend } from 'k6/metrics';

const tempoPostgres = new Trend('tempo_postgres');
const tempoNeo4j = new Trend('tempo_neo4j');

export const options = {
    scenarios: {
        teste_postgres: {
            executor: 'constant-vus',
            vus: 20,
            duration: '30s',
            exec: 'executarPostgres',
        },
        teste_neo4j: {
            executor: 'constant-vus',
            vus: 20,
            duration: '30s',
            startTime: '35s', 
            exec: 'executarNeo4j',
        },
    },
};

export function executarPostgres() {
    const userId = 1;
    const urlPostgres = `http://127.0.0.1:8000/recomendar/colaborativo/postgres/${userId}`;
    
    const res = http.get(urlPostgres);
    tempoPostgres.add(res.timings.duration);
    
    check(res, {
        'Postgres status e 200': (r) => r.status === 200,
    });
    
    sleep(0.1);
}

export function executarNeo4j() {
    const userId = 1;
    const urlNeo4j = `http://127.0.0.1:8000/recomendar/colaborativo/neo4j/${userId}`;
    
    const res = http.get(urlNeo4j);
    tempoNeo4j.add(res.timings.duration);
    
    check(res, {
        'Neo4j status e 200': (r) => r.status === 200,
    });
    
    sleep(0.1);
}