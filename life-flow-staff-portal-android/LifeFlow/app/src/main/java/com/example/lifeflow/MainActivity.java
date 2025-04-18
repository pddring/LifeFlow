package com.example.lifeflow;  // Ensure this matches your build.gradle namespace

import android.os.Bundle;
import android.view.View;
import android.view.inputmethod.InputMethodManager;
import android.widget.Button;
import android.widget.EditText;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.content.Context;

import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {

    WebView myWeb;
    EditText ipAddressInput;
    Button loadButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Initialize the views
        myWeb = findViewById(R.id.myWeb);
        ipAddressInput = findViewById(R.id.ipAddressInput);
        loadButton = findViewById(R.id.loadButton);

        // Enable JavaScript in WebView
        myWeb.getSettings().setJavaScriptEnabled(true);
        myWeb.setWebViewClient(new WebViewClient() {
            @Override
            public void onPageFinished(WebView view, String url) {
                // Once the WebView is loaded, hide system bars
                hideSystemBars();
            }
        });

        // Set onClickListener for the load button
        loadButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // Get the IP address from EditText
                String ipAddress = ipAddressInput.getText().toString().trim();

                // Check if the IP address is not empty
                if (!ipAddress.isEmpty()) {
                    // Load the IP address in the WebView, ensure it has the 'http://' prefix
                    myWeb.loadUrl("http://" + ipAddress);

                    // Hide the EditText and Button after loading the IP
                    ipAddressInput.setVisibility(View.GONE);
                    loadButton.setVisibility(View.GONE);

                    // Hide the keyboard
                    hideKeyboard();
                } else {
                    // Optionally, you can show a message if the input is empty
                    ipAddressInput.setError("Please enter a valid IP address");
                }
            }
        });
    }

    // Method to hide system bars and make the app fullscreen
    private void hideSystemBars() {
        // Hide the status bar and the navigation bar to create a fullscreen experience
        getWindow().getDecorView().setSystemUiVisibility(
                View.SYSTEM_UI_FLAG_IMMERSIVE
                        | View.SYSTEM_UI_FLAG_FULLSCREEN
                        | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                        | View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                        | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                        | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
        );
    }

    // Method to hide the keyboard
    private void hideKeyboard() {
        InputMethodManager imm = (InputMethodManager) getSystemService(Context.INPUT_METHOD_SERVICE);
        if (imm != null) {
            // Dismiss the keyboard
            imm.hideSoftInputFromWindow(ipAddressInput.getWindowToken(), 0);
        }
    }
}
