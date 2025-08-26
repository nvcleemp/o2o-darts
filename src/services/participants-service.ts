import { openDB } from 'idb';

const DB_NAME = 'darts-db';
const STORE_NAME = 'participants';
const DB_VERSION = 1;

export async function getDB() {
  return openDB(DB_NAME, DB_VERSION, {
    upgrade(db) {
      if (!db.objectStoreNames.contains(STORE_NAME)) {
        db.createObjectStore(STORE_NAME);
      }
    },
  });
}

export async function getParticipant(index: number): Promise<string> {
  const db = await getDB();
  return (await db.get(STORE_NAME, index)) || '';
}

export async function setParticipant(index: number, name: string): Promise<void> {
  const db = await getDB();
  await db.put(STORE_NAME, name, index);
}

export async function getAllParticipants(max: number): Promise<string[]> {
  const db = await getDB();
  const tx = db.transaction(STORE_NAME, 'readonly');
  const store = tx.objectStore(STORE_NAME);
  const result: string[] = [];
  for (let i = 0; i < max; i++) {
    result.push((await store.get(i)) || '');
  }
  await tx.done;
  return result;
}
