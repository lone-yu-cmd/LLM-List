package llmlist

import (
	"fmt"
	"testing"
)

func TestLoadRegistry(t *testing.T) {
	fmt.Println("Running Go SDK Verification...")
	reg, err := LoadRegistry()
	if err != nil {
		t.Fatalf("Failed to load registry: %v", err)
	}

	if len(reg.Providers) == 0 {
		t.Fatal("Providers should not be empty")
	}
	fmt.Printf("✓ Loaded %d providers\n", len(reg.Providers))
}

func TestGetProvider(t *testing.T) {
	required := []string{"openai", "anthropic"}
	for _, id := range required {
		p, err := GetProvider(id)
		if err != nil {
			t.Fatalf("Error getting provider %s: %v", id, err)
		}
		if p == nil {
			t.Fatalf("Provider %s should exist", id)
		}
		fmt.Printf("✓ Found provider: %s\n", p.Name)
	}
}

func TestGetAllChatModels(t *testing.T) {
	models, err := GetAllChatModels()
	if err != nil {
		t.Fatalf("Error getting chat models: %v", err)
	}
	if len(models) == 0 {
		t.Fatal("Should have chat models")
	}
	fmt.Printf("✓ Loaded %d chat models\n", len(models))
	fmt.Println("Go SDK Verification Passed!")
}
