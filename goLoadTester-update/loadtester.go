package main

import (
    "fmt"
    "net/http"
    "sync"
    "time"
)

const (
    TARGET_URL        = "http://odoo.acquirespot.xyz" 
    DURATION          = 2 * time.Minute         
    CONCURRENT_USERS  = 50
    REQUEST_INTERVAL  = 1 * time.Second
)


var (
    totalRequests      int64
    successfulRequests int64
    failedRequests     int64
    wg                 sync.WaitGroup
    mutex              sync.Mutex
)

func makeRequest(client *http.Client, stopTime time.Time) {
    for time.Now().Before(stopTime) {
        resp, err := client.Get(TARGET_URL)
        mutex.Lock()
        totalRequests++
        if err != nil {
            failedRequests++
            fmt.Printf("Error: %v\n", err)
            mutex.Unlock()
            time.Sleep(REQUEST_INTERVAL)
            continue
        }

        if resp.StatusCode == 200 {
            successfulRequests++
            fmt.Printf("Success Request: %d\n", resp.StatusCode)
        } else {
            failedRequests++
            fmt.Printf("Failled Request: %d\n", resp.StatusCode)
        }
        resp.Body.Close()
        mutex.Unlock()

        time.Sleep(REQUEST_INTERVAL)
    }
    wg.Done()
}

func main() {
    startTime := time.Now()
    stopTime := startTime.Add(DURATION)

    fmt.Printf("Start Load Testing %s with\n", TARGET_URL)
    fmt.Printf("Times: %v\n", DURATION)
    fmt.Printf("Users: %d\n", CONCURRENT_USERS)

    client := &http.Client{
        Timeout: 10 * time.Second,
    }

    
    for i := 0; i < CONCURRENT_USERS; i++ {
        wg.Add(1)
        go makeRequest(client, stopTime)
    }

    
    ticker := time.NewTicker(10 * time.Second)
    go func() {
        for t := range ticker.C {
            if t.After(stopTime) {
                ticker.Stop()
                return
            }
            elapsed := t.Sub(startTime)
            remaining := stopTime.Sub(t)
            fmt.Printf("Extended Time: %v, Remaining Time: %v\n", elapsed, remaining)
        }
    }()

    wg.Wait()

    
    fmt.Println("\nLoad Test done!")
    fmt.Printf("Total Request: %d\n", totalRequests)
    fmt.Printf("Success Request: %d\n", successfulRequests)
    fmt.Printf("Failled Request: %d\n", failedRequests)
    successRate := float64(successfulRequests) / float64(totalRequests) * 100
    fmt.Printf("Successfull rate: %.2f%%\n", successRate)
}