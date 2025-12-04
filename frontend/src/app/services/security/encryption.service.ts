import { Injectable } from "@angular/core";
import * as CryptoJS from 'crypto-js';
import { environment } from "src/environments/environment";

@Injectable({
    providedIn: 'root'
})
export class EncryptionService {
    key: string = "z!!!!!!!1sdfadsf56adf456asdfasdf";
    appProperties = {
        VALUES: {
            KEY: "MTIzNDU2Nzg5MEFCQ0RFRkdISUpLTE1O",
            IV: "MTIzNDU2Nzg="
        }
    }

    constructor() { }

    encryptionAES(msg: any) {
        // Encrypt
        const ciphertext = CryptoJS.AES.encrypt(msg, 'secret key 123');
        return ciphertext.toString();
    }

    decryptionAES(msg: any) {
        // Decrypt
        const bytes = CryptoJS.AES.decrypt(msg, 'secret key 123');
        const plaintext = bytes.toString(CryptoJS.enc.Utf8);
        return plaintext;
    }

    /** FUNCIONES DE ENCRIPTACION Y DESENCRIPTACION */

    decrypt(encryptedData: string): string {
        if (!environment.encryptation.enabled) {
            return encryptedData;
        }
        const parts = encryptedData.split(":");
        // Encoding the Salt in from UTF8 to byte array
        const Salt = CryptoJS.enc.Base64.parse(parts[0]);
        // Creating the Vector Key
        const iv = CryptoJS.enc.Base64.parse(parts[1]);
        // Encoding the Password in from UTF8 to byte array
        const Pass = CryptoJS.enc.Utf8.parse(
            environment.encryptation.key.trim()
        );
        // Creating the key in PBKDF2 format to be used during the decryption
        const key256Bits1000Iterations = CryptoJS.PBKDF2(
            Pass.toString(CryptoJS.enc.Utf8),
            Salt,
            { keySize: 256 / 32, iterations: 1000 }
        );
        // Enclosing the test to be decrypted in a CipherParams object as supported by the CryptoJS libarary
        const cipherParams = CryptoJS.lib.CipherParams.create({
            ciphertext: CryptoJS.enc.Base64.parse(parts[2]),
        });

        // Decrypting the string contained in cipherParams using the PBKDF2 key
        const decrypted = CryptoJS.AES.decrypt(
            cipherParams,
            key256Bits1000Iterations,
            { mode: CryptoJS.mode.CBC, iv: iv, padding: CryptoJS.pad.Pkcs7 }
        );
        const decryptedText = decrypted.toString(CryptoJS.enc.Utf8);

        return decryptedText;
    }

    encrypt(plainText: string): string {
        if (!environment.encryptation.enabled) {
            return plainText;
        }

        // Encoding the Salt in from UTF8 to byte array
        const Salt = CryptoJS.lib.WordArray.random(32);
        // Creating the Vector Key
        const Iv = CryptoJS.lib.WordArray.random(16);
        // Encoding the Password in from UTF8 to byte array
        const Pass = CryptoJS.enc.Utf8.parse(
            environment.encryptation.key.trim()
        );
        // Creating the key in PBKDF2 format to be used during the decryption
        const key256Bits1000Iterations = CryptoJS.PBKDF2(
            Pass.toString(CryptoJS.enc.Utf8),
            Salt,
            { keySize: 256 / 32, iterations: 1000 }
        );

        // Decrypting the string contained in cipherParams using the PBKDF2 key
        const encrypted = CryptoJS.AES.encrypt(
            plainText,
            key256Bits1000Iterations,
            { mode: CryptoJS.mode.CBC, iv: Iv }
        );

        const encryptedText = CryptoJS.enc.Base64.stringify(
            encrypted.ciphertext
        );
        const cipherWithSaltAndIv =
            CryptoJS.enc.Base64.stringify(Salt) +
            ":" +
            CryptoJS.enc.Base64.stringify(Iv) +
            ":" +
            encryptedText;

        return cipherWithSaltAndIv
            .replace(/\+/g, "p1L2u3S")
            .replace(/\//g, "s1L2a3S4h")
            .replace(/=/g, "e1Q2u3A4l");
    }
    decryptV2(encryptedData: string): string {
        if (!environment.encryptation.enabled) {
            return encryptedData;
        }
        return CryptoJS.AES.decrypt(encryptedData, environment.encryptation.key.trim()).toString(CryptoJS.enc.Utf8);
    }

    encryptV2(plainText: string): string {
        if (!environment.encryptation.enabled) {
            return plainText;
        }
        return CryptoJS.AES.encrypt(plainText,  environment.encryptation.key.trim()).toString();
    }
    encryptKey(key:string):string{
        return this.convertLetterToNumber(key).toString();
    }
    private convertLetterToNumber(str: string):number{
        let out = 0, len = str.length;
        for (let pos = 0; pos < len; pos++) {
            out += (str.charCodeAt(pos) - 64) * Math.pow(26, len - pos - 1);
        }
        return out;
    }

}
