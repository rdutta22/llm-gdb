#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void vulnerable_function(char *user_input) {
    char buffer[16];  // Small buffer - only 16 bytes
    
    printf("Buffer address: %p\n", (void*)buffer);
    printf("Copying %zu bytes into 16-byte buffer...\n", strlen(user_input));
    
    strcpy(buffer, user_input);
    
    printf("Buffer contents: %s\n", buffer);
    printf("Copy completed successfully!\n");
}

void unsafe_gets_example() {
    char buffer[32];
    
    printf("\nEnter some text (unsafe gets): ");
    gets(buffer);
    
    printf("You entered: %s\n", buffer);
}

void stack_corruption_demo(char *input) {
    int important_variable = 12345;
    char buffer[8];
    
    printf("\nBefore overflow:\n");
    printf("  important_variable = %d (at %p)\n", 
           important_variable, (void*)&important_variable);
    printf("  buffer at %p\n", (void*)buffer);
    
    strcpy(buffer, input);
    
    printf("\nAfter overflow:\n");
    printf("  important_variable = %d (corrupted!)\n", important_variable);
    
    if (important_variable != 12345) {
        printf("Memory corruption detected!\n");
    }
}

void heap_overflow_demo(char *input) {
    char *heap_buffer = (char*)malloc(16);
    
    printf("\nHeap buffer address: %p\n", (void*)heap_buffer);
    
    strcpy(heap_buffer, input);
    
    printf("Heap buffer: %s\n", heap_buffer);
    
    free(heap_buffer);
}

void print_usage(char *prog_name) {
    printf("Usage: %s <input_string>\n", prog_name);
    printf("\nExamples:\n");
    printf("  Safe:       %s \"Hello\"\n", prog_name);
    printf("  Overflow:   %s \"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\"\n", prog_name);
    printf("  Corruption: %s \"$(python -c 'print(\"A\"*50)')\"\n", prog_name);
    printf("\nTip: Try inputs of different lengths to see the overflow!\n");
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        print_usage(argv[0]);
        return 1;
    }
    
    char *user_input = argv[1];
    size_t input_len = strlen(user_input);
    
    printf("Input length: %zu bytes\n", input_len);
    printf("Input: \"%s\"\n\n", user_input);
    
    // Warning for long inputs
    if (input_len > 16) {
        printf("⚠️  WARNING: Input is %zu bytes, buffer is only 16 bytes!\n", 
               input_len);
        printf("⚠️  This WILL cause a buffer overflow!\n\n");
    }
    
    printf("═══ Test 1: Basic Buffer Overflow ═══\n");
    vulnerable_function(user_input);
    
    printf("\n═══ Test 2: Stack Corruption ═══\n");
    stack_corruption_demo(user_input);
    
    printf("\n═══ Test 3: Heap Overflow ═══\n");
    heap_overflow_demo(user_input);
    
    printf("\n✓ Program completed (somehow survived!)\n");
    
    return 0;
}
