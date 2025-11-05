package main

import (
    "fmt"
    "io"
    "net/http"
    "sync"
    "time"
)

type Result struct {
    StatusCode int
    Duration   time.Duration
    Error      error
}

func worker(id int, url string, requests int, wg *sync.WaitGroup, results chan<- Result) {
    defer wg.Done()
    for i := 0; i < requests; i++ {
        start := time.Now()
        resp, err := http.Get(url)
        duration := time.Since(start)

        if err != nil {
            results <- Result{StatusCode: 0, Duration: duration, Error: err}
            continue
        }

        // Drain body to reuse TCP connection
        _, _ = io.Copy(io.Discard, resp.Body)
        resp.Body.Close()

        results <- Result{StatusCode: resp.StatusCode, Duration: duration, Error: nil}
    }
}

func main() {
    var url string
    fmt.Println("Enter your IP or Link (with http or https): ")
    fmt.Scan(&url)
    totalRequests := 1000
    concurrency := 50

    var wg sync.WaitGroup
    results := make(chan Result, totalRequests)

    requestsPerWorker := totalRequests / concurrency

    start := time.Now()

    for i := 0; i < concurrency; i++ {
        wg.Add(1)
        go worker(i, url, requestsPerWorker, &wg, results)
    }

    wg.Wait()
    close(results)

    elapsed := time.Since(start)

    // Summary
    var success, failed int
    var totalTime time.Duration

    for r := range results {
        if r.Error != nil || r.StatusCode != 200 {
            failed++
        } else {
            success++
        }
        totalTime += r.Duration
    }

    avgTime := totalTime / time.Duration(totalRequests)

    fmt.Println("===== Load Test Summary =====")
    fmt.Printf("Target: %s\n", url)
    fmt.Printf("Total Requests: %d\n", totalRequests)
    fmt.Printf("Concurrency: %d\n", concurrency)
    fmt.Printf("Success: %d | Failed: %d\n", success, failed)
    fmt.Printf("Average Response Time: %v\n", avgTime)
    fmt.Printf("Total Test Duration: %v\n", elapsed)
}
