declare module 'crypto-js/sha256' {
  import { WordArray } from 'crypto-js'
  export default function SHA256(message: WordArray | string): WordArray
}
