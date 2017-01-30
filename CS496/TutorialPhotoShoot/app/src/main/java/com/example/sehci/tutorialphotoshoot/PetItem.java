package com.example.sehci.tutorialphotoshoot;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;

public class PetItem {
    public static PetItem deserialize(DataInputStream dis) throws IOException {
        PetItem pet = new PetItem();
        pet.setTxt(dis.readUTF());
        int photoLength = dis.readInt();
        if (photoLength < 0)
            photoLength = 0;
        byte[] photo = new byte[photoLength];
        dis.read(photo);
        pet.setPhoto(photo);
        return pet;
    }

    private byte[] photo;
    private String txt;

    private PetItem() {
    }

    public PetItem(String color, byte[] photo) {
        this.txt = color;
        this.photo = photo;
    }

    public byte[] getPhoto() {
        return photo != null ? photo : new byte[0];
    }

    public String getTxt() {
        return txt != null ? txt : "";
    }

    public void serialize(DataOutputStream dos) throws IOException {
        dos.writeUTF(getTxt());
        dos.writeInt(getPhoto().length);
        dos.write(getPhoto());
        dos.flush();
    }

    public void setPhoto(byte[] photo) {
        this.photo = photo;
    }

    public void setTxt(String txt) {
        this.txt = txt;
    }


}