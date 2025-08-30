package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
	"os/exec"
	"strconv"
)

func discreteLogHandler(w http.ResponseWriter, r *http.Request) {
	// CORS headers - allow requests from your frontend
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "GET, OPTIONS")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type")

	// Handle preflight requests
	if r.Method == "OPTIONS" {
		return
	}

	g := r.URL.Query().Get("g")
	h := r.URL.Query().Get("h")
	p := r.URL.Query().Get("p")

	if g == "" || h == "" || p == "" {
		http.Error(w, "Missing Query Parameters", http.StatusBadRequest)
		return
	}

	// Validate input parameters are integers
	if _, err := strconv.ParseInt(g, 10, 64); err != nil {
		http.Error(w, "Inputs must be integers", http.StatusBadRequest)
		return
	}
	if _, err := strconv.ParseInt(h, 10, 64); err != nil {
		http.Error(w, "Inputs must be integers", http.StatusBadRequest)
		return
	}
	if _, err := strconv.ParseInt(p, 10, 64); err != nil {
		http.Error(w, "Inputs must be integers", http.StatusBadRequest)
		return
	}

	// Execute Python script for Pohlig-Hellman algorithm
	cmd := exec.Command("python3", "pohlig_hellman.py", "--generator", g, "--element", h, "--modulus", p)
	output, err := cmd.CombinedOutput()
	if err != nil {
		log.Printf("Error running script: %v", err)
		http.Error(w, fmt.Sprintf("Error running script: %v", err), http.StatusInternalServerError)
		return
	}

	fmt.Fprintf(w, "%s", output)
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	fmt.Fprintf(w, `{"status": "healthy", "service": "discrete-log-calculator"}`)
}

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	http.HandleFunc("/discrete-log", discreteLogHandler)
	http.HandleFunc("/health", healthHandler)

	log.Printf("Discrete log calculator starting on port %s", port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}