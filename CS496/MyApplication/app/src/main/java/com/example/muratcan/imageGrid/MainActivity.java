package com.example.muratcan.imageGrid;

import android.graphics.Bitmap;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.widget.GridView;

import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {
    private GridView imageGrid;
    private ArrayList<Bitmap> bitmapList;
    private AsyncTask<String, Void, ArrayList<Bitmap>> task;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        this.imageGrid = (GridView) findViewById(R.id.gridView);
//        ImageView imageView= (ImageView) findViewById(R.id.imageView);
//        imageView.setImageBitmap(BitmapFactory.decodeFile(f.getAbsolutePath()));
        ImageAdapter imageAdapter = new ImageAdapter(this);
        this.imageGrid.setAdapter(imageAdapter);
    }
}
