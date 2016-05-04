package com.example.sehci.tutorialphotoshoot;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.provider.MediaStore;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        populateLast(loadLastPet());
    }


    /***********
     * CAPTURE PHOTO FROM CAMERA
     ******************/
    // Note: The method of saving images shown on
    // http://developer.android.com/training/camera/photobasics.html is
    // buggy on some devices, but we can get the byte[] directly, as shown
    // below

    static final int REQUEST_IMAGE_CAPTURE = 11111;

    public void displayCamera(View v) {
        Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        if (takePictureIntent.resolveActivity(getPackageManager()) != null) {
            startActivityForResult(takePictureIntent, REQUEST_IMAGE_CAPTURE);
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (requestCode == REQUEST_IMAGE_CAPTURE && resultCode == RESULT_OK) {
            // when camera returns
            Bundle extras = data.getExtras();
            imageBitmap = (Bitmap) extras.get("data");
            ImageView imgView = ((ImageView) findViewById(R.id.imgView));
            imgView.setImageBitmap(imageBitmap);
        }
    }

    private Bitmap imageBitmap;

    private byte[] getBytes(Bitmap bitmap) {
        if (bitmap == null || bitmap.getWidth() == 0 || bitmap.getHeight() == 0)
            return null;

        ByteArrayOutputStream bos = new ByteArrayOutputStream();
        try {
            bitmap.compress(Bitmap.CompressFormat.JPEG, 90, bos);
            bos.flush();
            bos.close();
        } catch (IOException ioe) {
            return null;
        }

        byte[] bytes = bos.toByteArray();
        return bytes != null && bytes.length > 0 ? bytes : null;
    }


    /***************
     * COLLECTING DATA INTO A PetItem OBJECT
     ***********/
    public void saveAndReset(View v) {
        // when user clicks save
        EditText txtColor = (EditText) findViewById(R.id.txtColor);

        StringBuffer err = new StringBuffer();

        final String color = txtColor.getText().toString();
        if (color == null || color.length() == 0)
            err.append("Color/name/info is blank");

        final byte[] photo = getBytes(imageBitmap);
        if (photo == null || photo.length == 0) {
            if (err.length() > 0)
                err.append("; ");
            err.append("Photo is missing");
        }

        if (err.length() > 0) {
            new AlertDialog.Builder(this)
                    .setTitle("Warning")
                    .setMessage(err + ". Continue?")
                    .setIcon(android.R.drawable.ic_dialog_alert)
                    .setPositiveButton(android.R.string.yes,
                            new DialogInterface.OnClickListener() {

                                public void onClick(DialogInterface dialog,
                                                    int whichButton) {
                                    saveAndReset0(color, photo);
                                }
                            }).setNegativeButton(android.R.string.no, null)
                    .show();
        } else {
            saveAndReset0(color, photo);
        }
    }

    private void saveAndReset0(String color, byte[] photo) {
        PetItem pet = new PetItem(color, photo);
        String err = writePetToFile(pet);

        Toast.makeText(this, err != null ? err : "Saved", Toast.LENGTH_SHORT).show();
        if (err == null) {
            populateLast(pet);
            ((EditText) findViewById(R.id.txtColor)).setText("");
            ((ImageView) findViewById(R.id.imgView)).setImageResource(R.mipmap.ic_launcher);
            imageBitmap = null;
        }
    }


    /***********
     * EVERYTHING RELATED TO FILE I/O
     ******************/
    // Note: for performance reasons, it would be reasonable to do this work in an AsyncTask
    private String writePetToFile(PetItem pet) {
        // create a unique, reasonable filename
        StringBuffer filename = new StringBuffer();
        filename.append(System.currentTimeMillis() + "-");
        String tmp = pet.getTxt();
        for (int i = 0; i < tmp.length(); i++) {
            char ch = tmp.charAt(i);
            if (Character.isLetterOrDigit(ch)) filename.append(ch);
            else filename.append("-");
            if (filename.length() >= 32) break;
        }

        // put the content in the right folder
        File file = new File(getFilesDir(), filename.toString());

        // and write the data to the file
        DataOutputStream dos = null;
        try {
            dos = new DataOutputStream(new FileOutputStream(file));
            pet.serialize(dos);
        } catch (IOException ex) {
            return ex.getMessage();
        } finally {
            try {
                if (dos != null) {
                    dos.flush();
                    dos.close();
                }
            } catch (IOException ex2) {
                ex2.printStackTrace();
            }
        }

        return null;
    }

    private PetItem loadLastPet() {
        File dir = getFilesDir();
        if (dir == null) return null;

        File[] allFiles = dir.listFiles();
        File lastFile = null;
        long lastDate = 0;
        if (allFiles != null) {
            for (File file : allFiles) {
                if (file != null && file.lastModified() > lastDate) {
                    lastFile = file;
                    lastDate = file.lastModified();
                }
            }
        }
        if (lastFile == null) return null;
        DataInputStream dis = null;
        try {
            dis = new DataInputStream(new FileInputStream(lastFile));
            return PetItem.deserialize(dis);
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        } finally {
            try {
                if (dis != null)
                    dis.close();
            } catch (IOException ex2) {
                ex2.printStackTrace();
            }
        }
    }

    private void populateLast(PetItem pet) {
        TextView txtLastColor = (TextView) findViewById(R.id.txtLastColor);
        ImageView imgLastView = (ImageView) findViewById(R.id.imgLastView);
        if (txtLastColor == null || imgLastView == null) return;

        String txt = pet != null ? pet.getTxt() : "";
        txtLastColor.setText(txt.length() > 0 ? "Recent: " + txt : "");

        byte[] photo = pet != null ? pet.getPhoto() : new byte[0];
        if (photo.length > 0) {
            Bitmap bitmap = BitmapFactory.decodeStream(new ByteArrayInputStream(photo));
            imgLastView.setImageBitmap(bitmap);
        } else {
            imgLastView.setImageResource(android.R.color.transparent);
        }
    }

}
