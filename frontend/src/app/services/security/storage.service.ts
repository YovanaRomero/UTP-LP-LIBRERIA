import { Injectable } from '@angular/core';
import { EncryptionService } from './encryption.service';
@Injectable({
  providedIn: 'root'
})
export class StorageService {

    constructor(private oEncryptionService: EncryptionService) { }

    setItem(name: string, value: any) {
      let newKey = this.oEncryptionService.encryptKey(name);
      localStorage.setItem(newKey, this.oEncryptionService.encryptV2(value.toString()).toString());
    }

    getItem(name: string): any {
      let keyEncrypted=this.oEncryptionService.encryptKey(name);
      let saved = localStorage.getItem(keyEncrypted);
      if(saved===null){
        return null;
      }
      return this.oEncryptionService.decryptV2(saved);
    }

    setObject(name: string, value: any) {
      let newKey = this.oEncryptionService.encryptKey(name);
      localStorage.setItem(newKey, this.oEncryptionService.encryptV2(JSON.stringify(value)).toString());
    }

    getObject(name: string): any {
      let keyEncrypted=this.oEncryptionService.encryptKey(name);
      let saved = localStorage.getItem(keyEncrypted);
      if(saved===null){
        return null;
      }
      let sDecryptedValue = this.oEncryptionService.decryptV2(saved);
      return JSON.parse(sDecryptedValue);
    }

    removeItem(name: string){
      let keyEncrypted=this.oEncryptionService.encryptKey(name);
      localStorage.removeItem(keyEncrypted);
    }

    removeAll(){
      localStorage.clear();
    }

  }
